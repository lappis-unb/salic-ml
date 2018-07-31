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


def is_project_num_items_outlier(pronac):
    projectList = ProjectsList(planilha_orcamentaria, planilha_comprovacao,
    planilha_captacao)

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
    projectList = ProjectsList(planilha_orcamentaria, planilha_comprovacao,
                               planilha_captacao)

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
