import pandas as pd
import numpy as np
import functools

from itertools import chain

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
    providers_count = data.providers_count.to_dict()[0]

    new_providers = {}
    segment_id = None

    for _, row in df.iterrows():
        cnpj = row['nrCNPJCPF']
        cnpj_count = providers_count.get(cnpj, 0)
        segment_id = row['idSegmento']

        if cnpj_count <= 1:
            item_id = row['idPlanilhaAprovacao']
            item_name = row['Item']
            provider_name = row['nmFornecedor']

            new_provider = new_providers.get(cnpj, None)

            if new_provider:
                new_provider['itens'][item_id] = {
                    'nome': item_name,
                    'tem_comprovante': True
                }

                new_provider['itens'] = {k: v for k, v in sorted(new_provider['itens'].items(), key=lambda i: i[1]['nome'])}

            else:
                new_provider = {
                    'nome': provider_name,
                    'cnpj': cnpj,
                    'itens': {
                        item_id: {
                            'nome': item_name,
                            'tem_comprovante': True
                        }
                    }
                }
            
            new_providers[cnpj] = new_provider

    new_providers = list(new_providers.values())
    providers_amount = len(df['nrCNPJCPF'].unique())

    new_providers_amount = len(new_providers)

    new_providers_percentage = new_providers_amount / providers_amount

    averages = data.average_percentage_of_new_providers.to_dict()
    segments_average = averages['segments_average_percentage']
    all_projects_average = list(averages['all_projects_average'].values())[0]
    if new_providers:
        new_providers.sort(key=lambda provider: provider['nome'])

    return {
        'lista_de_novos_fornecedores': new_providers,
        'valor': new_providers_amount,
        'new_providers_percentage': new_providers_percentage,
        'is_outlier': new_providers_percentage > segments_average[segment_id],
        'segment_average_percentage': segments_average[segment_id],
        'all_projects_average_percentage': all_projects_average,
    }


@data.lazy('providers_info', 'providers_count', 'all_providers_cnpj')
def average_percentage_of_new_providers(providers_info, providers_count, all_providers_cnpj):
    """
    Return the average percentage of new providers
    per segment and the average percentage of all projects.
    """
    providers_count = providers_count.to_dict()[0]
    all_providers_cnpj_tuples, _ = all_providers_cnpj
    
    partial_func = functools.partial(calc_new_providers_percentage, providers_count)
    percentages = all_providers_cnpj_tuples.apply(partial_func)

    return pd.DataFrame.from_dict(
        {
            'segments_average_percentage': percentages.groupby('idSegmento').mean(),
            'all_projects_average': percentages.mean()
        }
    )


@data.lazy('all_providers_cnpj')
def providers_count(df):
    """
    Returns total occurrences of each provider
    in the database.
    """
    _, cnpj_array = df
    unique, counts = np.unique(cnpj_array.values, return_counts=True)
    
    return pd.DataFrame.from_dict(dict(zip(unique, counts)), orient='index')


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
    Return all CNPJ/CPF of providers in the database.
    """
    series_of_lists = df.groupby(['PRONAC', 'idSegmento']).apply(lambda i: i['nrCNPJCPF'].unique())
    flatten = list(chain(*series_of_lists.values))
    return (series_of_lists, pd.DataFrame(flatten))


def get_providers_info(pronac):
    """
    Return all info about providers of a
    project with the given pronac.
    """
    df = data.providers_info
    grouped = df.groupby('PRONAC')

    return grouped.get_group(pronac)


def calc_new_providers_percentage(providers_count, array):
    new_providers = 0
    for cnpj in array:
        cnpj_count = providers_count.get(cnpj, 0)
        if cnpj_count <= 1:
            new_providers += 1

    new_providers_percent = new_providers / array.size
    return new_providers_percent