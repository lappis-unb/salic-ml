import os
import gc

import pandas as pd

from core.data_handler import data_source


dir_path = '/home/mandala/repos/minc/salic-ml/data/scripts'
csv_path = '/home/mandala/repos/minc/salic-ml/data/raw/'
files = ['planilha_captacao.sql', 'planilha_comprovacao.sql', 'planilha_orcamentaria.sql', 'planilha_projetos.sql']
files = [files[2]]


for file in files:
    print('Downloading: [{}]...'.format(file))
    path = os.path.join(dir_path, file)
    ds = data_source.DataSource(path)
    #pronac = '090105'
    pronac = '164274'
    pronac = None

    dataset = ds.get_dataset(pronac=pronac, use_cache=False)
    assert isinstance(dataset, pd.DataFrame)

    path = os.path.join(csv_path, file[:-4] + '_2.csv')
    dataset.to_csv(path)

    del dataset
    gc.collect()

'''
    dataset = ds.get_dataset(pronac=None, use_cache=True)
    print(dataset)

    dataset = ds.get_dataset(pronac=pronac, use_cache=False)
    print(dataset)

    pronac = '164274'
    dataset = ds.get_dataset(pronac=pronac, use_cache=True)
    print(dataset)
'''
