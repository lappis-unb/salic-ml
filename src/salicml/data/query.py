from collections import Mapping
from .loader import get_data


class InvalidMetricError(ValueError):
    """Raised when querying for an invalid metric."""


class Project(Mapping):
    """
    A immutable mapping from metric names to their corresponding value.

    Metrics can also be retrieved by attribute access.
    """

    def __init__(self, pronac, metrics):
        self.pronac = pronac
        self._metrics = metrics
        self._data = {}

    def __getitem__(self, item):
        try:
            return self._data[item]
        except KeyError:
            pass
        try:
            result = self._metrics.get_metric(self.pronac, item)
        except InvalidMetricError:
            raise KeyError(item)
        else:
            self._data[item] = result
            return result

    def __len__(self):
        return sum(1 for _ in self)

    def __iter__(self):
        return self._metrics.iter_metrics()

    def __getattr__(self, attr):
        if attr.startswith('_'):
            raise AttributeError(attr)
        try:
            return Namespace(self, attr)
        except KeyError:
            raise AttributeError(attr)


class Namespace:
    """
    A simple reference for a collection of metrics. It provides access to
    dotted metrics, e.g., ``project.finance.valor_aprovado``
    """
    def __init__(self, project, base):
        self._project = project
        self._base = base

    def __getattr__(self, attr):
        key = f'{self._base}.{attr}'
        try:
            return self._project[key]
        except KeyError:
            raise AttributeError(attr)


class Metrics:
    """
    Register all metrics in Salic-ML.
    """

    def __init__(self, data=get_data):
        self._data = get_data()
        self._metrics = {}

    def get_metric(self, pronac, metric):
        """
        Get metric for the project with the given pronac number.

        Usage:
            >>> metrics.get_metric(pronac_id, valor_aprovado """

        assert isinstance(metric, str)
        assert '.' in metric, 'metric must declare a namespace'

        try:
            func = self._metrics[metric]
            return func(pronac, self._data)
        except KeyError:
            raise InvalidMetricError('metric does not exist')

    def get_project(self, pronac):
        """Return a new object representing all metrics for a given project."""
        return Project(pronac, self)

    def iter_metrics(self):
        """Iterate over all metrics."""
        return iter(self._metrics)

    def register(self, category):
        """
        Usage:
            @metrics.register('finance')
            def valor_aprovado(data):
                return metric_from_data_and_pronac_number(data, pronac)
        """
        def decorator(func):
            name = func.__name__
            key = f'{category}.{name}'
            self._metrics[key] = func
            return func
        return decorator


# Global metrics attribute
metrics = Metrics()
from salicml.metrics import finance  # NOQA: F401, F403
