import pandas as pd
import numpy as np

from salicml.data.query import metrics
from salicml.data import data


@metrics.register('finance')
def novos_fornecedores(pronac, dt):
    """
    Return the percentage of providers of a project
    that are new to the providers database.
    """
    info = data.providers_info
    df = info[info['PRONAC'] == pronac]
    providers_quantity = data.providers_count.to_dict()[0]

    new_providers = []
    fdsa = []
    segment_id = None

    for _, row in df.iterrows():
        cnpj = row['nrCNPJCPF']
        cnpj_count = providers_quantity.get(cnpj, 0)
        segment_id = row['idSegmento']

        if cnpj_count <= 1:
            item_id = row['idPlanilhaAprovacao']
            item_name = row['Item']
            provider_name = row['nmFornecedor']

            new_provider = {
                'nome': provider_name,
                'cnpj': cnpj,
                'itens': [ 
                    {
                        'item_id': item_id,
                        'nome': item_name,
                        'tem_comprovante': True
                    }
                ]
            }

            append_new_provider = True
            append_new_item = True
            for provider in new_providers:
                if provider["nome"] == new_provider["nome"]:
                    append_new_provider = False
                    for item in provider["itens"]:
                        if new_provider["itens"][0]["item_id"] == item["item_id"]:
                            append_new_item = False
                        
                    if append_new_item: provider["itens"].append(new_provider["itens"][0])

            if append_new_provider:
                new_providers.append(new_provider)
            fdsa.append(new_provider)

    providers_amount = len(df['nrCNPJCPF'].unique())

    new_providers_amount = len(new_providers)

    new_providers_percentage = new_providers_amount / providers_amount

    averages = data.average_percentage_of_new_providers.to_dict()
    segments_average = averages['segments_average_percentage']
    all_projects_average = list(averages['all_projects_average'].values())[0]

    if new_providers:
        new_providers.sort(key=lambda provider: provider['nome'])

    return {
        'lista_': df['nrCNPJCPF'].unique(),
        'lista_de_novos': fdsa,
        'lista_de_novos_fornecedores': new_providers,
        'valor': providers_amount,
        'new_providers_percentage': new_providers_percentage,
        'is_outlier': new_providers_percentage > segments_average[segment_id],
        'segment_average_percentage': segments_average[segment_id],
        'all_projects_average_percentage': all_projects_average,
    }


@data.lazy('providers_info', 'providers_count')
def average_percentage_of_new_providers(providers_info, providers_count):
    """
    Return the average percentage of new providers
    per segment and the average percentage of all projects.
    """
    segments_percentages = {}
    all_projects_percentages = []
    providers_quantity = providers_count.to_dict()[0]

    for _, items in providers_info.groupby('PRONAC'):
        cnpj_array = items['nrCNPJCPF'].unique()
        new_providers = 0

        for cnpj in cnpj_array:
            cnpj_count = providers_quantity.get(cnpj, 0)
            if cnpj_count <= 1:
                new_providers += 1

        segment_id = items.iloc[0]['idSegmento']
        new_providers_percent = new_providers / cnpj_array.size
        segments_percentages.setdefault(segment_id, [])
        segments_percentages[segment_id].append(new_providers_percent)
        all_projects_percentages.append(new_providers_percent)

    segments_average_percentage = {}
    for segment_id, percentages in segments_percentages.items():
        mean = np.mean(percentages)
        segments_average_percentage[segment_id] = mean

    return pd.DataFrame.from_dict({
        'segments_average_percentage': segments_average_percentage,
        'all_projects_average': np.mean(all_projects_percentages)
    })


@data.lazy('all_providers_cnpj')
def providers_count(df):
    """
    Returns total occurrences of each provider
    in the database.
    """
    cnpjs = df.values
    unique, counts = np.unique(cnpjs, return_counts=True)
    providers_quantity = dict(zip(unique, counts))

    return pd.DataFrame.from_dict(providers_quantity, orient='index')


@data.lazy('planilha_comprovacao')
def providers_info(df):
    """
    Relevant info for providers.
    """
    return df[[
            "PRONAC", "IdPRONAC", "nrCNPJCPF",
            "DataProjeto", "idPlanilhaAprovacao",
            "Item", "nmFornecedor", "idSegmento",
            "UF", "cdProduto", "cdCidade",
            "idPlanilhaItem", "cdEtapa"
        ]]


@data.lazy('providers_info')
def all_providers_cnpj(df):
    """
    Return CPF/CNPJ of all providers
    in database.
    """
    cnpj_list = []
    for _, items in df.groupby('PRONAC'):
        cnpj_list += list(items['nrCNPJCPF'].unique())

    return pd.DataFrame(cnpj_list)


def get_providers_info(pronac):
    """
    Return all info about providers of a
    project with the given pronac.
    """
    df = data.providers_info
    grouped = df.groupby('PRONAC')

    return grouped.get_group(pronac)
