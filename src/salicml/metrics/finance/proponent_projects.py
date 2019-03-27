from salicml.data.query import metrics
from salicml.data import data
from salicml.metrics.base import get_cpf_cnpj_by_pronac

from functools import lru_cache


@metrics.register('finance')
def proponent_projects(pronac, data):
    """
    Checks the CNPJ/CPF of the proponent of project
    with the given pronac and returns all the projects
    that have been submitted by this proponent and all
    projects that have already been analyzed.
    """
    cpf_cnpj = get_cpf_cnpj_by_pronac(pronac)

    proponent_submitted_projects = {}
    proponent_analyzed_projects = {}

    if cpf_cnpj:
        submitted_projects = get_proponent_submitted_projects(cpf_cnpj)
        analyzed_projects = get_proponent_analyzed_projects(cpf_cnpj)

        try:
            proponent_submitted_projects = {
                'number_of_projects': submitted_projects['num_pronacs'],
                'pronacs_of_this_proponent': submitted_projects['pronac_list']
            }
        except KeyError:
            pass

        try:
            proponent_analyzed_projects = {
                'number_of_projects': analyzed_projects['num_pronacs'],
                'pronacs_of_this_proponent': analyzed_projects['pronac_list']
            }
        except KeyError:
            pass

    return {
        'cpf_cnpj': cpf_cnpj,
        'valor': len(proponent_submitted_projects),
        'projetos_submetidos': proponent_submitted_projects,
        'projetos_analizados': proponent_analyzed_projects,
    }


@data.lazy('verified_funds')
def analyzed_projects(raw_df):
    """
    Return all projects that was analyzed.
    """
    df = raw_df[['PRONAC', 'proponenteCgcCpf']]

    analyzed_projects = df.groupby('proponenteCgcCpf')[
        'PRONAC'
    ].agg(['unique', 'nunique'])

    analyzed_projects.columns = ['pronac_list', 'num_pronacs']

    return analyzed_projects


@data.lazy('planilha_projetos')
def submitted_projects(raw_df):
    """
    Return all submitted projects.
    """
    df = raw_df.astype({'PRONAC': str, 'CgcCpf': str})
    submitted_projects = df.groupby('CgcCpf')[
        'PRONAC'
    ].agg(['unique', 'nunique'])

    submitted_projects.columns = ['pronac_list', 'num_pronacs']

    return submitted_projects


@data.lazy('planilha_comprovacao')
def verified_funds(df):
    """
    Relevant info about proponent.
    """
    return (
        df[['PRONAC', 'proponenteCgcCpf']]
        .astype({'PRONAC': str, 'proponenteCgcCpf': str})
    )


@lru_cache(maxsize=128)
def submitted_projects_dict():
    """
    Cached dict of all submitted projects.
    """
    df = data.submitted_projects
    return df.to_dict(orient='index')


@lru_cache(maxsize=128)
def analyzed_projects_dict():
    """
    Cached dict of all analyzed projects.
    """
    df = data.analyzed_projects
    return df.to_dict(orient='index')


def get_proponent_submitted_projects(cpf_cnpj):
    """
    Returns all submitted projects of the proponent
    with the given CPF/CNPJ.
    """
    all_projects = submitted_projects_dict()
    try:
        return all_projects[str(cpf_cnpj)]
    except KeyError:
        return {}


def get_proponent_analyzed_projects(cpf_cnpj):
    """
    Returns all analyzed projects of the proponent
    with the given CPF/CNPJ.
    """
    all_projects = analyzed_projects_dict()
    try:
        return all_projects[str(cpf_cnpj)]
    except KeyError:
        return {}
