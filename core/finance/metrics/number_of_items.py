import numpy as np

class NumberOfItems():
    def __init__(self, items):
        """
            TODO.
        """
        items = items[['idSegmento', 'PRONAC', 'idPlanilhaAprovacao']]
        num_items = items.groupby(['idSegmento', 'PRONAC']).count()
        metrics = num_items.groupby('idSegmento').agg(['mean', 'std'])
        self.cache = metrics['idPlanilhaAprovacao'].to_dict('index')

    def get_metrics(self, pronac):
        return {}
