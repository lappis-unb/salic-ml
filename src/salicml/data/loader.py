import logging
import os
import pathlib
from functools import lru_cache

import pandas as pd

log = logging.getLogger("salic-ml.data")
LOG = log.info
FILE_EXTENSION = "pickle.gz"
READ_DF = pd.read_pickle
READ_DF_OPTS = {"compression": "infer"}
WRITE_DF = pd.DataFrame.to_pickle
WRITE_DF_OPTS = READ_DF_OPTS
ROOT = pathlib.Path(__file__).parent.parent.parent.parent / "data"
LOG = print


class Loader:
    """
    Lazily load raw data as dataframes.
    """

    def __init__(self, root=ROOT):
        self._root = pathlib.Path(root)
        self._cache = {}
        self._registry = {}

    def __getattr__(self, attr):
        try:
            return self._cache[attr]
        except KeyError:
            if attr in self._registry:
                df = self._registry[attr]()
            else:
                try:
                    df = _load_dataframe(self._root / "processed", attr)
                except FileNotFoundError:
                    df = _load_dataframe(self._root / "raw", attr)
            self._cache[attr] = df
            return df

    def __dir__(self):
        return sorted({
            *super().__dir__(),
            *self._cache,
            *self._registry,
            *_file_attributes(self._root / "processed"),
            *_file_attributes(self._root / "raw"),
        })

    def store(self, loc, df):
        """Store dataframe in the given location.

        Store some arbitrary dataframe:

        >>> data.store('my_data', df)

        Now recover it from the global store.
        >>> data.my_data
        ...
        """

        path = "%s.%s" % (self._root / "processed" / loc, FILE_EXTENSION)
        WRITE_DF(df, path, **WRITE_DF_OPTS)
        self._cache[loc] = df

    def lazy(self, *names, name=None):
        """

        Usage:

            >>> @data.lazy('area', 'planilha_orcamentaria')
            ... def orcamentaria_per_area(area, orcamentaria):
            ...     return new_dataframe()
        """

        def decorator(func):
            key = name or func.__name__

            def loader_function():
                if names:
                    args = [getattr(self, attr) for attr in names]
                else:
                    args = (self,)

                return func(*args)

            self._registry[key] = loader_function
            return func

        return decorator

    def clear(self):
        """Clear all cache information to free up memory."""

        self._cache.clear()


def _load_dataframe(root, attr):
    path = "%s.%s" % (root / attr, FILE_EXTENSION)
    return READ_DF(path, **READ_DF_OPTS)


def csv_to_pickle(path=ROOT / "raw", clean=False):
    """Convert all CSV files in path to pickle."""

    for file in os.listdir(path):
        base, ext = os.path.splitext(file)
        if ext != ".csv":
            continue

        LOG(f"converting {file} to pickle")
        df = pd.read_csv(path / file, low_memory=True)
        WRITE_DF(df, path / (base + "." + FILE_EXTENSION), **WRITE_DF_OPTS)
        if clean:
            os.remove(path / file)
            LOG(f"removed {file}")


def _file_attributes(path):
    base_ext = '.' + FILE_EXTENSION
    ext_size = len(base_ext)
    for file in os.listdir(path):
        if file.endswith(base_ext):
            yield file[:-ext_size]


@lru_cache(maxsize=128)
def get_data():
    return Loader()


data = Loader()
