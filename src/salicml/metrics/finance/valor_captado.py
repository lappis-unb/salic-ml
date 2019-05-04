from salicml.data.query import metrics
from salicml.data import data

import pandas as pd
import salicml.outliers.gaussian_outlier as gaussian_outlier


@metrics.register('finance')
def valor_captado(pronac, data):
    """
    Returns the total raised funds of a project
    with the given pronac and if this project is an
    outlier based on this value.
    """
    is_outlier, mean, std, total_raised_funds = get_outlier_info(pronac)
    maximum_expected_funds = gaussian_outlier.maximum_expected_value(mean, std)

    return {
        'is_outlier': is_outlier,
        'total_raised_funds': total_raised_funds,
        'maximum_expected_funds': maximum_expected_funds
    }


@data.lazy('all_raised_funds')
def raised_funds_by_segment(df):
    """
    Raised funds organized by segment.
    """
    return (
        df[['Pronac', 'Segmento', 'CaptacaoReal']]
        .groupby(['Segmento', 'Pronac'])
        .sum()
    )


@data.lazy('raised_funds_by_segment')
def segment_raised_funds_average(df):
    """
    Return some info about raised funds.
    """
    grouped = df.groupby('Segmento')
    aggregated = grouped.agg(['mean', 'std'])
    aggregated.columns = aggregated.columns.droplevel(0)

    return aggregated


def get_outlier_info(pronac):
    """
    Return if a project with the given
    pronac is an outlier based on raised funds.
    """
    df = data.planilha_captacao
    raised_funds_averages = data.segment_raised_funds_average.to_dict('index')

    segment_id = df[df['Pronac'] == pronac]['Segmento'].iloc[0]

    mean = raised_funds_averages[segment_id]['mean']
    std = raised_funds_averages[segment_id]['std']

    project_raised_funds = get_project_raised_funds(pronac)

    outlier = gaussian_outlier.is_outlier(project_raised_funds, mean, std)

    return (outlier, mean, std, project_raised_funds)


def get_project_raised_funds(pronac):
    """
    Return the total raised funds of a project
    with the given pronac.
    """
    return(
        data.raised_funds_by_project
        .loc[pronac]
        ['CaptacaoReal']
    )
