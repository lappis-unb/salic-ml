import numpy as np

class NumberOfItems():
    def __init__(self, orcamento):
        self.orcamento = orcamento
        self._init_cache()

    def _init_cache(self):
        self.cache = {}
        self.segments = self.orcamento['idSegmento'].unique
        for segment in self.segments:
            items = self.orcamento[self.orcamento['idSegmento'] == segment]
            pronacs = items['PRONAC'].unique

            num_items = []
            for pronac in pronacs:
                num_items.append(len(items[items['PRONAC'] == pronac]))

            self.cache[segment] = {
                'mean': np.mean(num_items),
                'std': np.std(num_items)
            }
