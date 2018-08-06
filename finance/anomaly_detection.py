import numpy as np

from finance.models.projects import Project, ProjectsList
from salicml.outliers import gaussian_outlier
from salicml.utils.read_csv import read_csv


planilha_orcamentaria_file_name  = 'planilha_orcamentaria.csv'
planilha_orcamentaria = read_csv(planilha_orcamentaria_file_name)

planilha_comprovacao_file_name  = 'planilha_comprovacao_2.csv'
planilha_comprovacao = read_csv(planilha_comprovacao_file_name)

planilha_captacao_file_name  = 'planilha_captacao.csv'
planilha_captacao = read_csv(planilha_captacao_file_name)


projectList = ProjectsList(planilha_orcamentaria, planilha_comprovacao,
                           planilha_captacao)

def is_project_num_items_outlier(pronac):
    project = projectList.loadSingleProject(pronac)
    segment, segment_id = project.segment
    project_num_items = project.items.get_number_of_items()
    print(project_num_items)
    
    projectList.loadFilteredProjects([('idSegmento', segment_id)])
    pronacs = projectList.pronac_list

    projects_number_of_items = [projectList.loaded_projects[pronac].items.get_number_of_items() for pronac in pronacs]
    
    mean = np.mean(projects_number_of_items)
    std = np.std(projects_number_of_items)
    
    is_outlier = gaussian_outlier.is_outlier(project_num_items, mean, std, 1.5)
    return is_outlier


def is_project_total_raised_outlier(pronac):
    project = projectList.loadSingleProject(pronac)
    segment, segment_id = project.segment

    total_raised = project.captacoes.get_total_real_raised_funds()

    projectList.loadFilteredProjects([('idSegmento', segment_id)])
    pronacs = projectList.pronac_list

    projects_raised_funds = np.array([projectList.loaded_projects[
                                          pronac].captacoes.get_total_real_raised_funds()
                                      for pronac in pronacs])
    projects_raised_funds = projects_raised_funds[projects_raised_funds != 0]

    mean = np.mean(projects_raised_funds)
    std = np.std(projects_raised_funds)

    is_outlier = gaussian_outlier.is_outlier(total_raised, mean, std, 1.5)
    return is_outlier


def is_project_total_verified_outlier(pronac):
    project = projectList.loadSingleProject(pronac)
    segment, segment_id = project.segment

    total_verified = project.receipts.get_total_verified_cost()

    projectList.loadFilteredProjects([('idSegmento', segment_id)])
    pronacs = projectList.pronac_list

    projects_verified_funds = np.array(
        [projectList.loaded_projects[pronac].receipts.get_total_verified_cost()
         for pronac in pronacs])
    projects_verified_funds = projects_verified_funds[
        projects_verified_funds != 0]

    mean = np.mean(projects_verified_funds)
    std = np.std(projects_verified_funds)

    is_outlier = gaussian_outlier.is_outlier(total_verified, mean, std, 1.5)
    return is_outlier


def is_project_total_approved_funds_outlier(pronac):
    project = projectList.loadSingleProject(pronac)
    segment, segment_id = project.segment

    total_approved = project.items.get_total_approved_cost()

    projectList.loadFilteredProjects([('idSegmento', segment_id)])
    pronacs = projectList.pronac_list

    projects_approved_funds = np.array(
        [projectList.loaded_projects[pronac].items.get_total_approved_cost()
         for pronac in pronacs])
    projects_approved_funds = projects_approved_funds[
        projects_approved_funds != 0]

    mean = np.mean(projects_approved_funds)
    std = np.std(projects_approved_funds)

    is_outlier = gaussian_outlier.is_outlier(total_approved, mean, std, 1.5)
    return is_outlier


def is_project_receipts_number_outlier(pronac):
    project = projectList.loadSingleProject(pronac)
    segment, segment_id = project.segment

    total_receipts = project.receipts.get_number_of_receipts()
    print('total receipts = {}'.format(total_receipts))

    projectList.loadFilteredProjects([('idSegmento', segment_id)])
    pronacs = projectList.pronac_list

    projects_receipts = np.array(
        [projectList.loaded_projects[pronac].receipts.get_number_of_receipts()
         for pronac in pronacs])
    projects_receipts = projects_receipts[projects_receipts != 0]
    if projects_receipts.shape[0] == 0:
        projects_receipts = [0]

    mean = np.mean(projects_receipts)
    std = np.std(projects_receipts)

    is_outlier = gaussian_outlier.is_outlier(total_receipts, mean, std, 1.5)
    return is_outlier