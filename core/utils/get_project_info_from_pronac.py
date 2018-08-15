from core.utils.read_csv import read_csv_with_different_type

class GetProjectInfoFromPronac():

    def __init__(self):
        csv_name = 'planilha_projetos.csv'
        usecols = ['PRONAC', 'NomeProjeto']
        self.projects_info_df = read_csv_with_different_type(csv_name, {'PRONAC':str}, usecols=usecols)
        self.projects_info_df.set_index('PRONAC', inplace=True)

    def get_projects_name(self, pronac_list):
        project_name = self.projects_info_df.loc[pronac_list, 'NomeProjeto']
        projects_name = project_name.to_dict()
        return projects_name