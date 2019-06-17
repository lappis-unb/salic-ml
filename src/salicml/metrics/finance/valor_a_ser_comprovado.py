import pandas as pd

from salicml.data.query import metrics
from salicml.data import data


# @data.lazy('planilha_captacao')
def raised_funds_by_project(df):
    """
    Raised funds organized by project.
    """
    df['CaptacaoReal'] = df['CaptacaoReal'].apply(
        pd.to_numeric
    )
    return (
        df[['Pronac', 'CaptacaoReal']]
        .groupby(['Pronac'])
        .sum()
    )


@metrics.register('finance')
def valor_a_ser_comprovado(pronac, dt):
    """
    Checks how much money is left for the project to verify,
    using valor_captado - valor_comprovado
    This value can be negative (a project can verify more money than
    the value approved)
    """
    project_raised_funds = data.raised_funds_by_project.loc[pronac]['CaptacaoReal']

    dataframe = data.planilha_comprovacao
    project_verified = dataframe.loc[dataframe['PRONAC'] == str(pronac)]
    if project_verified.empty:
        project_verified_funds = 0
    else:
        pronac_funds = project_verified[
            ["idPlanilhaAprovacao", "PRONAC", "vlComprovacao", "idSegmento"]
        ]
        funds_grp = pronac_funds.drop(columns=["idPlanilhaAprovacao"]).groupby(
            ["PRONAC"]
        )
        project_verified_funds = funds_grp.sum().loc[pronac]["vlComprovacao"]

    to_verify_value = project_raised_funds - float(project_verified_funds)
    is_outlier = to_verify_value != 0

    return {
        'is_outlier': is_outlier,
        'valor': to_verify_value,
        'valor_captado': project_raised_funds,
        'valor_comprovado': project_verified_funds,
        'minimo_esperado': 0,
    }
