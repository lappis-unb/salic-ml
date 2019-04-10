from salicml.data.query import metrics
from salicml.data import data
import numpy as np

COLUMNS = ['PRONAC', 'idComprovantePagamento', 'tpFormaDePagamento', 'Item',
           'nmFornecedor', 'vlComprovacao']
new_tpFormaDePagamento = {0.0: np.nan, 1.0: "Cheque",
                          2.0: "Transferência Bancária", 3.0: 'Saque/Dinheiro'}


@metrics.register('finance')
def check_receipts(pronac, dt):
    """
    Checks how many items are in a same receipt when payment type is check
        - is_outlier: True if there are any receipts that have more than one
        - itens_que_compartilham_comprovantes: List of items that share receipt
    """
    df = verified_repeated_receipts_for_pronac(pronac)
    comprovantes_cheque = df[df['tpFormaDePagamento'] == 1.0]

    return metric_return(comprovantes_cheque)


@metrics.register('finance')
def transfer_receipts(pronac, dt):
    """
    Checks how many items are in a same receipt when payment type is bank
    transfer
        - is_outlier: True if there are any receipts that have more than one
        - itens_que_compartilham_comprovantes: List of items that share receipt
    """
    df = verified_repeated_receipts_for_pronac(pronac)
    comprovantes_transferencia = df[df['tpFormaDePagamento'] == 2.0]

    return metric_return(comprovantes_transferencia)


@metrics.register('finance')
def money_receipts(pronac, dt):
    """
    Checks how many items are in a same receipt when payment type is
    withdraw/money
        - is_outlier: True if there are any receipts that have more than one
        - itens_que_compartilham_comprovantes: List of items that share receipt
    """
    df = verified_repeated_receipts_for_pronac(pronac)
    comprovantes_saque = df[df['tpFormaDePagamento'] == 3.0]

    return metric_return(comprovantes_saque)


@data.lazy('planilha_comprovacao')
def verified_repeated_receipts(df):
    receipts = df[COLUMNS]
    duplicated = receipts[receipts
                          .duplicated(subset=['idComprovantePagamento'],
                                      keep=False)]
    return duplicated


def verified_repeated_receipts_for_pronac(pronac):
    df = data.verified_repeated_receipts
    df = df[df['PRONAC'] == pronac]
    del df['PRONAC']
    return df


def metric_return(dataframe):
    is_outlier = None
    value = dataframe.shape[0]
    del dataframe['tpFormaDePagamento']
    if dataframe.empty:
        is_outlier = False
        dataframe = []
    else:
        dataframe = dataframe.to_dict('records')
        is_outlier = True
    return {
        'is_outlier': is_outlier,
        'valor': value,
        'itens_que_compartilham_comprovantes': dataframe,
    }
