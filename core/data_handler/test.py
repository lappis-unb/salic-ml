from core.data_handler import data_source
import os


dir_path = '/home/mandala/repos/minc/salic-ml/data/scripts'
files = ['planilha_captacao.sql', 'planilha_comprovacao.sql', 'planilha_orcamentaria.sql', 'planilha_projetos.sql']

files = [files[2]]

for file in files:
    print('Downloading: [{}]...'.format(file))
    path = os.path.join(dir_path, file)
    ds = data_source.DataSource(path)
    pronac = '164274'
    dataset = ds.get_dataset(pronac=None, use_cache=False)
    print(dataset)

    break

    dataset = ds.get_dataset(pronac=None, use_cache=True)
    print(dataset)

    dataset = ds.get_dataset(pronac=pronac, use_cache=False)
    print(dataset)

    pronac = '164274'
    dataset = ds.get_dataset(pronac=pronac, use_cache=True)
    print(dataset)
