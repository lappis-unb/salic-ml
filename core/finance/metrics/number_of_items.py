import os

from core.data_handler.data_source import DataSource

class NumberOfItems():
    def __init__(self, items):
        """
            This function receives a pandas.DataFrame with all items of all
            Salic projects and generate the mean and variance of the 'number of
            items' of the projects grouped by their artistical segment. It also
            caches the 'number of items' of each project.
            Input:
                items: pandas.Dataframe containing the all items of all
                       Salic projects. It must contain at least the columns
                       'idSegmento', 'PRONAC', and 'idPlanilhaAprovacao'.
            Output:
                This function has no output, instead, it caches the metrics
                found in its instance.
        """
        print('*** NumberOfItems ***')
        items = items[['idSegmento', 'PRONAC', 'idPlanilhaAprovacao']]
        num_items = items.groupby(['idSegmento', 'PRONAC']).count()
        metrics = num_items.groupby('idSegmento').agg(['mean', 'std'])
        self.cache = metrics['idPlanilhaAprovacao'].to_dict('index')
        self.cache['projects'] = num_items.reset_index('idSegmento')

    def get_metrics(self, pronac, k=1.5):
        """
            This function receives a project identifier and a constant 'k' and
            verify if this project has an anomalous 'number os items' in its
            budget spreadsheet, based on a gaussian distribution. The project
            is said outlier if its:
                (number of items) > (mean + k * std)
            for this segment. It also return the project 'number of items' and
            its segment 'mean' and 'standard deviation' for this metric.
            Input:
                pronac: the project identifier.
                k: constant that defines the threshold to verify if a project
                   is an outlier.
            Output:
                A dictionary containing the keys: is_outlier, value, mean, and
                std.
        """
        if not isinstance(pronac, str):
            raise ValueError('PRONAC type must be str')

        pronac_data = self._get_pronac_data(pronac)

        metrics = self.cache[pronac_data['segment_id']]
        threshold = metrics['mean'] + k * metrics['std']

        results = {}
        results['is_outlier'] = (pronac_data['items_count'] > threshold)
        results['value'] = pronac_data['items_count']
        results['mean'] = metrics['mean']
        results['std'] = metrics['std']

        return results

    def _get_pronac_data(self, pronac):

        __FILE__FOLDER = os.path.dirname(os.path.realpath(__file__))
        sql_folder = os.path.join(__FILE__FOLDER, os.pardir, os.pardir, os.pardir)
        sql_folder = os.path.join(sql_folder, 'data', 'scripts')

        datasource = DataSource()
        path = os.path.join(sql_folder, 'planilha_orcamentaria.sql')

        pronac_dataframe = datasource.get_dataset(path, pronac=pronac)

        pronac_data = {
            'segment_id': pronac_dataframe.iloc[0]['idSegmento'],
            'items_count': pronac_dataframe.shape[0]
        }


        return pronac_data