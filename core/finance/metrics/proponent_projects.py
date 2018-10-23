import os
import pandas as pd

from core.data_handler.data_source import DataSource

class ProponentProjects():
    """ This class is used to verify all the projects of a given proponent
    that have been submitted and/or analyzed.
    """

    def __init__(self, df_verified_funds, df_projects):
        """ All information needed to answer future requests to this class will
        be saved/cached in this function.
        The variables 'analyzed_projects' and 'submitted_projects' are dictionaries with
        CNPJ/CPF as key.

        Input:
                df_verified_funds: pandas.Dataframe with at least the columns 'PRONAC',
                and 'proponenteCgcCpf'.
                df_projects : pandas.Dataframe with at least the columns 'PRONAC',
                and 'CgcCpf'.
        """
        print('*** ProponentProjects ***')
        assert isinstance(df_verified_funds, pd.DataFrame)
        assert isinstance(df_projects, pd.DataFrame)

        self.df_verified_funds = df_verified_funds
        self.df_projects = df_projects

        [self.analyzed_projects, self.submitted_projects] = self._set_up_cache()



    def get_metrics(self, pronac):
        """ This function receives a project identifier as parameter. Then, it checks the
        CNPJ/CPF of it's proponent and returns all the projects that have been submitted by
        this proponent and all projects that have already been analyzed.

            Input:
                pronac: the project identifier.

            Output:
                A dictionary containing the keys:
                    - cnpj_cpf, submitted_projects, analyzed_projects.

                    'submitted_projects' is a dictionary with the keys:
                        - number_of_projects, pronacs_of_this_proponent

                    'analyzed_projects' is a dictionary with the keys:
                        - number_of_projects, pronacs_of_this_proponent
        """
        if not isinstance(pronac, str):
            raise ValueError('PRONAC type must be str')

        cnpj_cpf = self._get_pronac_data(pronac)

        submitted = {}
        submitted['number_of_projects'] = 0
        submitted['pronacs_of_this_proponent'] = []

        if cnpj_cpf in self.submitted_projects.keys():
            submitted['number_of_projects'] = self.submitted_projects[cnpj_cpf]['num_pronacs']
            submitted['pronacs_of_this_proponent'] = self.submitted_projects[cnpj_cpf]['pronacs_list']

        analyzed = {}
        analyzed['number_of_projects'] = 0
        analyzed['pronacs_of_this_proponent'] = []

        if cnpj_cpf in self.analyzed_projects.keys():
            analyzed['number_of_projects'] = self.analyzed_projects[cnpj_cpf]['num_pronacs']
            analyzed['pronacs_of_this_proponent'] = self.analyzed_projects[cnpj_cpf]['pronacs_list'].tolist()

        metric_information = {}
        metric_information['cnpj_cpf'] = cnpj_cpf
        metric_information['submitted_projects'] = submitted
        metric_information['analyzed_projects'] = analyzed

        return metric_information


    def get_cnpj_cpf_by_pronac(self, pronac):
        """ Receives the project identifier as parameter and returns the CPF/CNPJ
        of the proponent of the given project.
        """
        cnpj_cpf = 'CNPJ/CPF NOT FOUND'
        cnpj_cpf_df = self.df_projects.loc[self.df_projects['PRONAC'] == pronac, ['CgcCpf']]
        if not cnpj_cpf_df.empty:
            cnpj_cpf = cnpj_cpf_df.iloc[0, 0]
        return cnpj_cpf


    def _set_up_cache(self):
        """ Builds the dictionaries used as cache.
        """
        filtered_verified_funds = self.df_verified_funds[['PRONAC', 'proponenteCgcCpf']]
        analyzed_projects = filtered_verified_funds.groupby(['proponenteCgcCpf'])['PRONAC'] \
            .agg(['unique', 'nunique'])
        analyzed_projects.columns = ['pronacs_list', 'num_pronacs']
        analyzed_projects = analyzed_projects.to_dict('index')


        filtered_projects = self.df_projects[['PRONAC', 'CgcCpf']]
        submitted_projects = filtered_projects.groupby(['CgcCpf'])['PRONAC'] \
            .agg(['unique', 'nunique'])
        submitted_projects.columns = ['pronacs_list', 'num_pronacs']
        submitted_projects = submitted_projects.to_dict('index')

        return [analyzed_projects, submitted_projects]

    def _get_pronac_data(self, pronac):
        __FILE__FOLDER = os.path.dirname(os.path.realpath(__file__))
        sql_folder = os.path.join(__FILE__FOLDER, os.pardir, os.pardir, os.pardir)
        sql_folder = os.path.join(sql_folder, 'data', 'scripts')

        datasource = DataSource()
        path = os.path.join(sql_folder, 'planilha_projetos.sql')

        pronac_dataframe = datasource.get_dataset(path, pronac=pronac)

        cnpj_cpf = 'CNPJ/CPF NOT FOUND'
        cnpj_cpf_df = pronac_dataframe.loc[pronac_dataframe['PRONAC'] == pronac, ['CgcCpf']]
        if not cnpj_cpf_df.empty:
            cnpj_cpf = cnpj_cpf_df.iloc[0, 0]

        return cnpj_cpf