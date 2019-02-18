import pandas as pd
import salicml.outliers.gaussian_outlier as gaussian_outlier

from salicml.data.query import metrics
from salicml.data import data


@metrics.register('finance')
def verified_funds(pronac, data):
    """
    Responsable for detecting anomalies in projects total verified funds.
    """
    dataframe = data.planilha_comprovacao
    project = dataframe.loc[dataframe['PRONAC'] == pronac]
    segment_id = project.iloc[0]["idSegmento"]
    pronac_funds = project[
        ["idPlanilhaAprovacao", "PRONAC", "vlComprovacao", "idSegmento"]
    ]
    funds_grp = pronac_funds.drop(columns=["idPlanilhaAprovacao"]).groupby(
        ["PRONAC"]
    )
    project_funds = funds_grp.sum().loc[pronac]["vlComprovacao"]

    segments_info = data.verified_funds_by_segment_agg.to_dict(orient="index")
    mean = segments_info[segment_id]["mean"]
    std = segments_info[segment_id]["std"]
    is_outlier = gaussian_outlier.is_outlier(project_funds, mean, std)
    maximum_expected_funds = gaussian_outlier.maximum_expected_value(mean, std)
    return {
            "is_outlier": is_outlier,
            "total_verified_funds": project_funds,
            "maximum_expected_funds": maximum_expected_funds,
    }


@data.lazy('planilha_comprovacao')
def comprovation_value(df):
    df["vlComprovacao"] = df["vlComprovacao"].apply(
        pd.to_numeric
    )
    return df


@data.lazy('comprovation_value')
def verified_funds_by_segment_agg(df):
    df = (
        df[["PRONAC", "idSegmento", "vlComprovacao"]]
        .groupby(["idSegmento", "PRONAC"])
        .sum()
    )

    df = df.groupby(["idSegmento"])
    df = df.agg(
        ["count", "sum", "mean", "std"]
    )

    df.columns = df.columns.droplevel(0)
    return df
