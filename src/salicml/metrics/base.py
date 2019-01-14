from salicml.data import data


def get_info(df, group, info=['mean', 'std']):
    agg = df.groupby(group).agg(info)
    agg.columns = agg.columns.droplevel(0)
    return agg


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