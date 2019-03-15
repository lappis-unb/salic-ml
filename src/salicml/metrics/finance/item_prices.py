from salicml.outliers import gaussian_outlier
from salicml.data.query import metrics
from salicml.data import data
from salicml.metrics.base import get_salic_url, has_receipt

import pandas as pd
import numpy as np
from datetime import datetime


@metrics.register('finance')
def item_prices(pronac, data):
    """
    Verify if a project is an outlier compared
    to the other projects in his segment, based
    on the price of bought items.
    """
    threshold = 0.1

    outlier_info = get_outliers_percentage(pronac)
    outlier_info['is_outlier'] = outlier_info['percentage'] > threshold
    outlier_info['maximum_expected'] = threshold * outlier_info['total_items']

    return outlier_info


def is_outlier(df, item_id, segment_id, price):
    """
    Verify if a item is an outlier compared to the
    other occurrences of the same item, based on his price.

    Args:
        item_id: idPlanilhaItens
        segment_id: idSegmento
        price: VlUnitarioAprovado
    """

    if (segment_id, item_id) not in df.index:
        return False

    mean = df.loc[(segment_id, item_id)]['mean']
    std = df.loc[(segment_id, item_id)]['std']

    return gaussian_outlier.is_outlier(
        x=price, mean=mean, standard_deviation=std
    )


@data.lazy('relevant_items')
def aggregated_relevant_items(raw_df):
    """
    Aggragation for calculate mean and std.
    """
    df = (
        raw_df[['idSegmento', 'idPlanilhaItens', 'VlUnitarioAprovado']]
        .groupby(by=['idSegmento', 'idPlanilhaItens'])
        .agg([np.mean, lambda x: np.std(x, ddof=0)])
    )
    df.columns = df.columns.droplevel(0)
    return (
        df
        .rename(columns={'<lambda>': 'std'})
    )


@data.lazy('items_with_price')
def relevant_items(df):
    """
    Dataframe with items used by cultural projects,
    filtered by date and price.
    """
    start_date = datetime(2013, 1, 1)

    df['DataProjeto'] = pd.to_datetime(df['DataProjeto'])

    # get only projects newer than start_date
    # and items with price > 0
    df = df[df.DataProjeto >= start_date]
    df = df[df.VlUnitarioAprovado > 0.0]

    return df


@data.lazy('planilha_orcamentaria')
def items_with_price(raw_df):
    """
    Dataframe with price as number.
    """
    df = (
        raw_df
        [['PRONAC', 'idPlanilhaAprovacao', 'Item',
            'idPlanilhaItens', 'VlUnitarioAprovado',
            'idSegmento', 'DataProjeto', 'idPronac',
            'UfItem', 'idProduto', 'cdCidade', 'cdEtapa']]
    ).copy()

    df['VlUnitarioAprovado'] = df['VlUnitarioAprovado'].apply(pd.to_numeric)
    return df


def get_outliers_percentage(pronac):
    """
    Returns the percentage of items
    of the project that are outliers.
    """
    items = (
        data.items_with_price
        .groupby(['PRONAC'])
        .get_group(pronac)
    )

    df = data.aggregated_relevant_items

    outlier_items = {}
    url_prefix = '/prestacao-contas/analisar/comprovante'

    for _, item in items.iterrows():
        item_id = item['idPlanilhaItens']
        price = item['VlUnitarioAprovado']
        segment_id = item['idSegmento']
        item_name = item['Item']

        if is_outlier(df, item_id, segment_id, price):
            outlier_items[item_id] = {
                'name': item_name,
                'salic_url': get_salic_url(item, url_prefix),
                'has_receipt': has_receipt(item)
            }

    total_items = items.shape[0]
    outliers_amount = len(outlier_items)

    percentage = outliers_amount / total_items

    return {
        'items': outlier_items,
        'valor': outliers_amount,
        'total_items': total_items,
        'percentage': percentage,
    }
