import numpy as np
import pandas as pd
from salicml.data import data
from salicml.data.query import metrics
from salicml.metrics.base import get_segment_id, get_segment_projects
from functools import lru_cache


@metrics.register('finance')
def common_items_ratio(pronac, data):
    """
    Calculates the common items on projects in a cultural segment,
    calculates the uncommon items on projects in a cultural segment and
    verify if a project is an outlier compared to the other projects
    in his segment.
    """
    segment_id = get_segment_id(pronac)
    ratio = common_items_percentage(pronac, segment_id)
    metrics = data.common_items_metrics.to_dict(orient='index')[segment_id]

    # constant that defines the threshold to verify if a project
    # is an outlier.
    k = 1.5

    threshold = metrics['mean'] - k * metrics['std']

    uncommon_items = get_uncommon_items(pronac)

    pronac_filter = data.all_items['PRONAC'] == pronac
    uncommon_items_filter = (
        data.all_items['idPlanilhaItens']
        .isin(uncommon_items)
    )
    items_filter = (pronac_filter & uncommon_items_filter)

    filtered_items = (
        data
        .all_items[items_filter]
        .drop_duplicates(subset='idPlanilhaItens')
    )
    uncommon_items = add_info_to_uncommon_items(filtered_items, uncommon_items)

    return {
        'is_outlier': ratio < threshold,
        'value': ratio,
        'mean': metrics['mean'],
        'std': metrics['std'],
        'uncommon_items': uncommon_items,
        'common_items_not_present': get_common_items_not_present(pronac),
    }


@data.lazy('all_items', 'common_items')
def common_items_metrics(all_items, common_items):
    """
    Calculates the percentage of common items for each project
    in each segment and calculates the mean and std of this percentage
    for each segment.
    """
    segments = common_items.index.unique()
    metrics = {}
    for seg in segments:
        common_items = segment_common_items(seg)
        projects = get_segment_projects(seg)

        metric_values = []

        for proj in projects:
            pronac = proj[0]
            percentage = common_items_percentage(pronac, seg)
            metric_values.append(percentage)

        metrics[seg] = {
            'mean': np.mean(metric_values),
            'std': np.std(metric_values)
        }

    return pd.DataFrame.from_dict(metrics, orient='index')


@data.lazy('all_items')
def common_items(df):
    """
    Returns the itens that are common in all the segments,
    in the format | idSegmento | id planilhaItens |.
    """
    percentage = 0.1

    return (
        df
        .groupby(['idSegmento', 'idPlanilhaItens'])
        .count()
        .rename(columns={'PRONAC': 'itemOccurrences'})
        .sort_values('itemOccurrences', ascending=False)
        .reset_index(['idSegmento', 'idPlanilhaItens'])
        .groupby('idSegmento')
        .apply(lambda x: x[None: max(2, int(len(x) * percentage))])
        .reset_index(['idSegmento'], drop=True)
        .set_index(['idSegmento'])
    )


@data.lazy('planilha_orcamentaria')
def distinct_items(df):
    """
    Returns a dataframe with all itens with no duplicates
    in the format | idPlanilhaItens | Item |.
    """
    return (
        df
        [['idPlanilhaItens', 'Item']]
        .set_index('idPlanilhaItens')
        .drop_duplicates()
    )


@data.lazy('planilha_orcamentaria')
def all_items(df):
    """
    Return all itens used in the segments, with no duplicates.
    """
    return (
        df[['PRONAC', 'idSegmento', 'idPlanilhaItens', 'idPronac',
            'UfItem', 'idProduto', 'cdCidade', 'cdEtapa']]
        .drop_duplicates()
    )


@data.lazy('planilha_comprovacao')
def receipt(df):
    """
    Return a dataframe to verify if a item has a receipt.
    """
    mutated_df = df[['IdPRONAC', 'idPlanilhaItem']].astype(str)
    mutated_df['pronac_planilha_itens'] = (
        f"{mutated_df['IdPRONAC']}/{mutated_df['idPlanilhaItem']}"
    )

    return (
        mutated_df
        .set_index(['pronac_planilha_itens'])
    )


@lru_cache(maxsize=128)
def get_project_items(pronac):
    """
    Returns all items from a project.
    """
    df = data.all_items
    return (
        df[df['PRONAC'] == pronac]
        .drop(columns=['PRONAC', 'idSegmento'])
    )


@lru_cache(maxsize=128)
def segment_common_items(segment_id):
    """
    Returns all the common items in a segment.
    """
    df = data.common_items
    return (
        df
        .loc[str(segment_id)]
        .reset_index(drop=1)
        .drop(columns=["itemOccurrences"])
    )


@lru_cache(maxsize=128)
def common_items_percentage(pronac, segment_id):
    """
    Returns the percentage of items in a project that are
    common in the cultural segment.
    """
    seg_common_items = segment_common_items(segment_id)

    if len(seg_common_items) == 0:
        return 0

    project_items = get_project_items(pronac).values[:, 0]
    project_items_amount = len(project_items)

    if project_items_amount == 0:
        return 1

    common_found_items = sum(
        seg_common_items.isin(project_items)['idPlanilhaItens']
    )

    return common_found_items / project_items_amount


@lru_cache(maxsize=128)
def get_uncommon_items(pronac):
    """
    Return all uncommon items of a project
    (related to segment common items).
    """
    segment_id = get_segment_id(pronac)
    seg_common_items = (
        segment_common_items(segment_id)
        .set_index('idPlanilhaItens')
        .index
    )
    project_items = (
        get_project_items(pronac)
        .set_index('idPlanilhaItens')
        .index
    )

    diff = list(project_items.difference(seg_common_items))

    return (
        data.distinct_items
        .loc[diff]
        .to_dict()['Item']
    )


@lru_cache(maxsize=128)
def get_common_items_not_present(pronac):
    """
    Returns all segment common items that are not
    present in the project.
    """
    segment_id = get_segment_id(pronac)
    seg_common_items = (
        segment_common_items(segment_id)
        .set_index('idPlanilhaItens')
        .index
    )
    project_items = (
        get_project_items(pronac)
        .set_index('idPlanilhaItens')
        .index
    )
    diff = list(seg_common_items.difference(project_items))

    return (
        data.distinct_items
        .loc[diff]
        .to_dict()['Item']
    )


def add_info_to_uncommon_items(filtered_items, uncommon_items):
    """
    Add extra info to the uncommon items.
    """

    result = uncommon_items

    for _, item in filtered_items.iterrows():
        item_id = item['idPlanilhaItens']
        item_name = uncommon_items[item_id]

        result[item_id] = {
            'name': item_name,
            'salic_url': get_salic_url(item),
            'has_recepit': has_recepit(item)
        }

    return result


def has_recepit(item):
    """
    Verify if a item has a receipt.
    """
    pronac_id = str(item['idPronac'])
    item_id = str(item["idPlanilhaItens"])

    combined_id = f'{pronac_id}/{item_id}'

    return combined_id in data.receipt.index


def get_salic_url(item):
    """
    Mount a salic url for the given item.
    """
    url_keys = {
        'pronac': 'idPronac',
        'uf': 'uf',
        'product': 'produto',
        'county': 'idmunicipio',
        'item_id': 'idPlanilhaItem',
        'stage': 'etapa',
    }

    url_values = {
        "pronac": item["idPronac"],
        "uf": item["UfItem"],
        "product": item["idProduto"],
        "county": item["cdCidade"],
        "item_id": item["idPlanilhaItens"],
        "stage": item["cdEtapa"],
    }

    item_data = [(value, url_values[key]) for key, value in url_keys.items()]
    url = '/prestacao-contas/analisar/comprovante'
    for k, v in item_data:
        url += f'/{str(k)}/{str(v)}'

    return url
