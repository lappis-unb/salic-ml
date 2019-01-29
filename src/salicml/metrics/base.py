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
