from salicml.data.query import metrics
from salicml.data import data
import numpy as np
import toolz

COLUMNS = [
    'PRONAC', 'idComprovantePagamento', 'tpFormaDePagamento', 'Item',
    'nmFornecedor', 'vlComprovacao', 'nrCNPJCPF'
]
COLUMNS_RENAME = {
    'nmFornecedor': 'nome_fornecedor',
    'Item': 'item',
    'vlComprovacao': 'valor_comprovado',
    'nrCNPJCPF': 'cpf_cnpj_fornecedor',
}
new_tpFormaDePagamento = {
    '0': np.nan,
    '1': "Cheque",
    '2': "Transferência Bancária",
    '3': 'Saque/Dinheiro'
}


@metrics.register('finance')
def comprovante_cheque(pronac, dt):
    """
    Checks how many items are in a same receipt when payment type is check
        - is_outlier: True if there are any receipts that have more than one
        - itens_que_compartilham_comprovantes: List of items that share receipt
    """
    df = verified_repeated_receipts_for_pronac(pronac)
    comprovantes_cheque = df[df['tpFormaDePagamento'] == '1']

    return metric_return(comprovantes_cheque)


@metrics.register('finance')
def comprovante_transferencia(pronac, dt):
    """
    Checks how many items are in a same receipt when payment type is bank
    transfer
        - is_outlier: True if there are any receipts that have more than one
        - itens_que_compartilham_comprovantes: List of items that share receipt
    """
    df = verified_repeated_receipts_for_pronac(pronac)
    comprovantes_transferencia = df[df['tpFormaDePagamento'] == '2']

    return metric_return(comprovantes_transferencia)


@metrics.register('finance')
def comprovante_saque(pronac, dt):
    """
    Checks how many items are in a same receipt when payment type is
    withdraw/money
        - is_outlier: True if there are any receipts that have more than one
        - itens_que_compartilham_comprovantes: List of items that share receipt
    """
    df = verified_repeated_receipts_for_pronac(pronac)
    comprovantes_saque = df[df['tpFormaDePagamento'] == '3']

    return metric_return(comprovantes_saque)


@data.lazy('planilha_comprovacao')
def verified_repeated_receipts(df):
    receipts = df[COLUMNS]
    duplicated = receipts[receipts.duplicated(
        subset=['idComprovantePagamento'], keep=False)]
    return duplicated


def verified_repeated_receipts_for_pronac(pronac):
    df = data.verified_repeated_receipts
    df = df[df['PRONAC'] == pronac]
    del df['PRONAC']
    return df


def metric_return(dataframe):
    is_outlier = None
    results = {}
    del dataframe['tpFormaDePagamento']
    if dataframe.empty:
        is_outlier = False
        dataframe = []
    else:
        dataframe.rename(columns=COLUMNS_RENAME, inplace=True)
        results = dataframe.to_dict('records')
        results = toolz.groupby('idComprovantePagamento', results)
        is_outlier = True

    return {
        'is_outlier': is_outlier,
        'valor': len(results),
        'comprovantes': add_keys(results),
    }


def add_keys(results):

    modified_dict_list = []
    for key in results.keys():
        modified_dict_list.append({
            "id_comprovante": key,
            "itens": results[key]
        })

    return modified_dict_list
