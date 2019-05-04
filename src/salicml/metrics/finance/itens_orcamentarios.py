from salicml.data.query import metrics
from salicml.data import data
from salicml.metrics.base import get_info


@metrics.register('finance')
def itens_orcamentarios(pronac, dt):
    """
    This metric calculates the project number of declared number of items
    and compare it to projects in the same segment
    output:
            is_outlier: True if projects number of items is not compatible
                        to others projects in the same segment
            valor: absolute number of items
            maximo_esperado: mean number of items of segment
            desvio_padrao: standard deviation of number of items in project segment
    """
    df = data.items_by_project
    project = df.loc[df['PRONAC'] == pronac]
    seg = project.iloc[0]["idSegmento"]
    info = data.items_by_project_agg.to_dict(orient="index")[seg]
    mean, std = info.values()
    threshold = mean + 1.5 * std
    project_items_count = project.shape[0]
    is_outlier = project_items_count > threshold
    return {
       'is_outlier': is_outlier,
       'valor': project_items_count,
       'maximo_esperado': mean,
       'desvio_padrao': std,
    }


@data.lazy('planilha_orcamentaria')
def items_by_project(df):
    """
    Return a dataframe to verify project number of items
    """
    df = df[["idSegmento", "PRONAC", "idPlanilhaAprovacao"]]
    return df


@data.lazy('items_by_project')
def items_by_project_agg(df):
    """
    Return Agreggate mean and standard deviantion of project number of items
    """
    return get_info(df.groupby(["idSegmento", "PRONAC"]).count(), 'idSegmento')
