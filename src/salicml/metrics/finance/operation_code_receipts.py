from salicml.data.query import metrics
from salicml.data import data
import numpy as np

COLUMNS = ['PRONAC', 'idComprovantePagamento', 'tpFormaDePagamento', 'Item',
           'nmFornecedor', 'vlComprovacao']
new_tpFormaDePagamento = {0.0: np.nan, 1.0: "Cheque",
                          2.0: "Transferência Bancária", 3.0: 'Saque/Dinheiro'}


@metrics.register('finance')
def operation_code_receipts(pronac, dt):
    df = data.verified_repeated_receipts
    df = df[df['PRONAC'] == pronac]
    comprovantes_cheque = df[df['tpFormaDePagamento'] == 1.0]
    comprovantes_transferencia = df[df['tpFormaDePagamento'] == 2.0]
    comprovantes_saque = df[df['tpFormaDePagamento'] == 3.0]

    return {
        "receipts_check": metric_return(comprovantes_cheque),
        "receipts_transfer": metric_return(comprovantes_transferencia),
        "receipts_money": metric_return(comprovantes_saque),
    }


@data.lazy('planilha_comprovacao')
def verified_repeated_receipts(df):
    receipts = df[COLUMNS]
    duplicated = receipts[receipts
                          .duplicated(subset=['idComprovantePagamento'],
                                      keep=False)]
    return duplicated


def metric_return(dataframe):
    is_outlier = None
    del dataframe['tpFormaDePagamento']
    if dataframe.empty:
        is_outlier = False
        dataframe = []
    else:
        is_outlier = True
    return {
        'is_outlier': is_outlier,
        'itens_que_compartilham_comprovantes': dataframe,
    }
