from core.utils.read_csv import read_csv_with_different_type

class GetProjectInfoFromPronac():

    def __init__(self):
        csv_name = 'planilha_projetos.csv'
        usecols = ['PRONAC', 'NomeProjeto', 'IdPRONAC']
        self.projects_info_df = read_csv_with_different_type(csv_name, {'PRONAC':str}, usecols=usecols)
        self.projects_info_df.set_index('PRONAC', inplace=True)

    def get_projects_name(self, pronac_list):
        project_name = self.projects_info_df.loc[pronac_list, 'NomeProjeto']
        projects_name = project_name.to_dict()
        return projects_name

    def get_projects_name_and_url(self, pronac_list):
        project_name_id = self.projects_info_df.loc[pronac_list, ['NomeProjeto', 'IdPRONAC']]
        project_name_id['IdPRONAC'] = 'prestacao-contas/prestacao-contas/tipo-avaliacao/idPronac/' + \
                                      project_name_id['IdPRONAC'].astype(str)
        project_name_id.columns = ['NomeProjeto', 'URL']
        projects_dict = project_name_id.to_dict('index')
        return projects_dict
