import numpy as np
import salicml.outliers.gaussian_outlier as gaussian_outlier

from salicml.data.query import metrics
from salicml.data import data


@metrics.register('finance')
def comprovante_pagamento(pronac, dt):
    """
    This metric calculates the project total of receipts
    and compare it to projects in the same segment
    output:
            is_outlier: True if projects receipts is not compatible
                        to others projects in the same segment
            comprovante_pagamento: absolute number of receipts
            maximum_expected_in_segment: maximum receipts expected in segment
    """
    dataframe = data.planilha_comprovacao
    project = dataframe.loc[dataframe['PRONAC'] == pronac]

    segment_id = project.iloc[0]["idSegmento"]
    segments_cache = data.segment_projects_agg
    segments_cache = segments_cache.to_dict(orient="index")

    mean = segments_cache[segment_id]["mean"]
    std = segments_cache[segment_id]["<lambda>"]
    total_receipts = project.shape[0]
    is_outlier = gaussian_outlier.is_outlier(total_receipts, mean, std)
    maximum_expected = gaussian_outlier.maximum_expected_value(mean, std)
    return {
            "is_outlier": is_outlier,
            "valor": total_receipts,
            "maximo_esperado": maximum_expected,
            "minimo_esperado": 0,
        }


@data.lazy('planilha_comprovacao')
def segment_projects(df):
    return df.groupby(["idSegmento", "PRONAC"]).nunique()


@data.lazy('segment_projects')
def segment_projects_agg(df):
    df = df["idComprovantePagamento"].groupby(["idSegmento"])

    return df.agg([np.mean, lambda x: np.std(x, ddof=0)])
