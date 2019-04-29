import numpy as np
import pandas as pd

from salicml.data import data
from salicml.data.query import metrics
from salicml.metrics.base import (
    get_salic_url, get_segment_id, get_segment_projects, has_receipt
)

from functools import lru_cache


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


def common_items_percentage(pronac, seg_common_items):
    """
    Returns the percentage of items in a project that are
    common in the cultural segment.
    """
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
        seg_common_items = segment_common_items(seg)
        projects = get_segment_projects(seg)

        metric_values = []

        for proj in projects:
            pronac = proj[0]
            percentage = common_items_percentage(pronac, seg_common_items)
            metric_values.append(percentage)

        metrics[seg] = {
            'mean': np.mean(metric_values),
            'std': np.std(metric_values)
        }
    return pd.DataFrame.from_dict(metrics, orient='index')


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
def get_uncommon_items(pronac):
    """
    Return all uncommon items of a project
    (related to segment common items).
    """
    segment_id = get_segment_id(str(pronac))
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
    segment_id = get_segment_id(str(pronac))
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
    url_prefix = '/prestacao-contas/analisar/comprovante'

    for _, item in filtered_items.iterrows():
        item_id = item['idPlanilhaItens']
        item_name = uncommon_items[item_id]

        result[item_id] = {
            'name': item_name,
            'salic_url': get_salic_url(item, url_prefix),
            'has_recepit': has_receipt(item)
        }

    return result


@metrics.register('finance')
def itens_comuns_e_incomuns_por_segmento(pronac, dt):
    """
    Calculates the common items on projects in a cultural segment,
    calculates the uncommon items on projects in a cultural segment and
    verify if a project is an outlier compared to the other projects
    in his segment.
    """
    segment_id = get_segment_id(str(pronac))
    metrics = data.common_items_metrics.to_dict(orient='index')[segment_id]
    ratio = common_items_percentage(pronac, segment_common_items(segment_id))

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
        'valor': ratio,
        'maximo_esperado': metrics['mean'],
        'desvio_padrao': metrics['std'],
        'items_incomuns': uncommon_items,
        'items_comuns_que_o_projeto_nao_possui': get_common_items_not_present(pronac),
    }
