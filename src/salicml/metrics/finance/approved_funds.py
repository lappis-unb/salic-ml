import os
import pandas as pd
import numpy as np
import salicml.outliers.gaussian_outlier as gaussian_outlier

from salicml.data.data_source import DataSource

from salicml.data.query import metrics
from salicml.metrics import base


@metrics.register('finance')
def approved_funds(pronac, data):
    """
    Verifica se o valor total de um projeto é um outlier em relação
    aos projetos do mesmo seguimento cultural.

    Dataframes: planilha_orcamentaria
    """

    main_df = data.planilha_orcamentaria
    funds_df = data.approved_funds_by_projects
    
    project = funds_df.loc[funds_df['PRONAC'] == int(pronac)].to_dict('records')[0]
    
    info = data.approved_funds_agg.to_dict(orient="index")[project['idSegmento']]

    mean, std = info.values()


    outlier = gaussian_outlier.is_outlier(project['VlTotalAprovado'], mean, std)
    maximum_expected_funds = gaussian_outlier.maximum_expected_value(mean, std)

    return {
       'is_outlier': outlier,
       'total_approved_funds': project['VlTotalAprovado'],
       'maximum_expected_funds': maximum_expected_funds
    }

