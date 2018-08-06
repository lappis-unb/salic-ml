import numpy as np

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
        items = items[['idSegmento', 'PRONAC', 'idPlanilhaAprovacao']]
        num_items = items.groupby(['idSegmento', 'PRONAC']).count()
        metrics = num_items.groupby('idSegmento').agg(['mean', 'std'])
        self.cache = metrics['idPlanilhaAprovacao'].to_dict('index')
        self.cache['projects'] = num_items.reset_index('idSegmento')

    def get_metrics(self, pronac, k=1.5):
        """
            This function receives a project identifier and a constant 'k' and
            verify if this project has an anomalous 'number os items' in its
            budget spreadsheet, based on a gaussian distribution. The project is
            said outlier if its 'number of items' is greater than 'mean + k*std'
            of its segment. It also return the project 'number of items' and its
            segment 'mean' and 'standard deviation'.
            Input:
                pronac: the project identifier.
                k: constant that defines the threshold to verify if a project is
                   an outlier.
            Output:
                A dictionary containing the keys: is_outlier, value, mean, and
                std.
        """
        project = self.cache['projects'].loc[pronac]
        metrics = self.cache[project['idSegmento']]
        threshold = metrics['mean'] + k * metrics['std']

        results = {}
        results['is_outlier'] = (project['idPlanilhaAprovacao'] > threshold)
        results['value'] = project['idPlanilhaAprovacao']
        results['mean'] = metrics['mean']
        results['std'] = metrics['std']

        return results
