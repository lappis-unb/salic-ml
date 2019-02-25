import salicml.outliers.gaussian_outlier as gaussian_outlier

from salicml.data.query import metrics
from salicml.data import data
from salicml.metrics.base import get_info


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


@metrics.register('finance')
def approved_funds(pronac, dt):
    """
    Verifica se o valor total de um projeto é um
    outlier em relação
    aos projetos do mesmo seguimento cultural
    Dataframes: planilha_orcamentaria
    """
    funds_df = data.approved_funds_by_projects

    project = (
        funds_df
        .loc[funds_df['PRONAC'] == pronac]
    )
    project = project.to_dict('records')[0]
    info = (
        data
        .approved_funds_agg.to_dict(orient="index")
        [project['idSegmento']]
    )

    mean, std = info.values()

    outlier = gaussian_outlier.is_outlier(project['VlTotalAprovado'],
                                          mean, std)
    maximum_expected_funds = gaussian_outlier.maximum_expected_value(mean, std)

    return {
        'is_outlier': outlier,
        'total_approved_funds': project['VlTotalAprovado'],
        'maximum_expected_funds': maximum_expected_funds
    }
