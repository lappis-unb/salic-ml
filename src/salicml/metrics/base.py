from salicml.data import data
from functools import lru_cache


def get_info(df, group, info=['mean', 'std']):
    """
    Aggregate mean and std with the given group.
    """
    agg = df.groupby(group).agg(info)
    agg.columns = agg.columns.droplevel(0)
    return agg


def get_segment_id(pronac):
    """
    Returns the cultural segment of the
    project with the given pronac.
    """
    df = data.planilha_orcamentaria
    return (
        df[df['PRONAC'] == int(pronac)]
        .iloc[0]['idSegmento']
    )


def get_salic_url(item, prefix):
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
    url = prefix
    for k, v in item_data:
        url += f'/{str(k)}/{str(v)}'

    return url


def has_receipt(item):
    """
    Verify if a item has a receipt.
    """
    pronac_id = str(item['idPronac'])
    item_id = str(item["idPlanilhaItens"])

    combined_id = f'{pronac_id}/{item_id}'

    return combined_id in data.receipt.index


@lru_cache(maxsize=128)
def get_segment_projects(segment_id):
    """
    Returns all projects from a segment.
    """
    df = data.all_items
    return (
        df[df['idSegmento'] == str(segment_id)]
        .drop_duplicates(["PRONAC"])
        .values
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


@data.lazy('planilha_orcamentaria')
def approved_funds_by_segments(df):
    df = df[["PRONAC", "idSegmento", "VlTotalAprovado"]]
    return df.groupby(['idSegmento', 'PRONAC']).sum()


@data.lazy('approved_funds_by_segments')
def approved_funds_agg(df):
    return get_info(df, 'idSegmento')


@data.lazy('planilha_orcamentaria')
def approved_funds_by_projects(df):
    return df[['PRONAC', 'idSegmento', 'VlTotalAprovado']] \
            .groupby(['PRONAC', 'idSegmento']).sum() \
            .reset_index()
