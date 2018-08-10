import pandas as pd

class ProponentProjects():

    def __init__(self, df_verified_funds, df_projects):

        assert isinstance(df_verified_funds, pd.DataFrame)
        assert isinstance(df_projects, pd.DataFrame)

        self.df_verified_funds = df_verified_funds
        self.df_projects = df_projects

        [self.analyzed_projects, self.submitted_projects] = self._set_up_cache()



    def get_metrics(self, pronac):

        submitted = {}
        submitted['number_of_projects'] = 0
        submitted['pronacs_of_this_proponent'] = []

        if pronac in self.submitted_projects.keys():
            submitted['number_of_projects'] = self.submitted_projects[pronac]['num_pronacs']
            submitted['pronacs_of_this_proponent'] = self.submitted_projects[pronac]['pronacs_list']

        analyzed = {}
        analyzed['number_of_projects'] = 0
        analyzed['pronacs_of_this_proponent'] = []

        if pronac in self.analyzed_projects.keys():
            analyzed['number_of_projects'] = self.analyzed_projects[pronac]['num_pronacs']
            analyzed['pronacs_of_this_proponent'] = self.analyzed_projects[pronac]['pronacs_list'].tolist()

        metric_information = {}
        metric_information['submitted_projects'] = submitted
        metric_information['analyzed_projects'] = analyzed

        return metric_information


    def _set_up_cache(self):
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
