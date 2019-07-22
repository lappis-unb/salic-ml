from invoke import task
import pandas as pd
import os
import sys

from src.salicml.data import csv_to_pickle, data
from src.salicml.data.db_operations import save_sql_to_files, save_sql_to_file, save_dataframe_as_pickle
from src.salicml.data.ftp_updater import execute_upload_pickle

python = sys.executable
sys.path.append('src')


#
# Call python manage.py in a more robust way
#
def manage(ctx, cmd, env=None, **kwargs):
    ags = {k.replace('_', '-'): v for k, v in kwargs.items() if v is not False}
    opts = ' '.join(f'--{k} {"" if v is True else v}' for k, v in ags.items())
    cmd = f'{python} src/salicml_api/manage.py {cmd} {opts}'
    env = {**os.environ, **(env or {})}
    path = env.get("PYTHONPATH", ":".join(sys.path))
    env.setdefault('PYTHONPATH', f'src:{path}')
    ctx.run(cmd, pty=True, env=env)


@task
def run(ctx):
    """
    Run development server
    """
    os.system('service cron start')
    manage(ctx, 'runserver 0.0.0.0:8000', env={})


@task
def make(ctx):
    """
    Make project migrations
    """
    manage(ctx, 'makemigrations', env={})


@task
def migrate(ctx):
    """
    Excute project migrations
    """
    manage(ctx, 'migrate', env={})


@task
def pickle(ctx, clean=False):
    """
    Converts csv files in data/raw/ to pickle files
    args:
        clean: if True removes csv files after conversion
    """
    csv_to_pickle(clean=clean)


@task
def train_metrics(ctx):
    """
    Trains the projects financial indicator metrics,
    using api models information
    """
    manage(ctx, 'update_projects_metrics', env={})


@task(help={'f': "Default is False, force to save files even if already exists"})
def get_pickles(ctx, f=False):
    """
    Updates local django db projects and pickle files using salic database from
    MinC
    Pickles are saved in /data/raw/ from sql queries in /data/scripts/
    """
    save_sql_to_files(f)


@task(help={'f': "Default is False, force to update model even if already exists"})
def update_models(ctx, f=False):
    """
    Updates local django db projects models using salic database from
    MinC
    """
    if f:
        manage(ctx, 'create_models_from_sql --force True', env={})
    else:
        manage(ctx, 'create_models_from_sql', env={})


@task
def run_sql(ctx, sql_file, dest):
    """
    Runs a sql script file and saves its result as a pickle
    Example of usage:
        $ inv run-sql --sql-file='./data/scripts/planilha_projetos.sql' --dest='.'
    """
    save_sql_to_file(sql_file, dest)


@task(help={'file': 'Pickle file path'})
def update_ftp(ctx, file):
    """
    Uploads pickle file to ftp /data/ folder
    """
    execute_upload_pickle(file)


@task
def gen_test_df(ctx):
    """
    Generate small dataframes that represents the
    real dataframes used in metrics training. 
    """
    print('Generating test dataframes...\n')

    print('Generating test planilha orcamentaria...')
    # planilha orcamentaria
    df_name = 'planilha_orcamentaria'
    df_orcamentaria = pd.DataFrame()
    for seg in data.planilha_orcamentaria.idSegmento.unique():
        is_seg = data.planilha_orcamentaria['idSegmento'] == seg
        df_orcamentaria = pd.concat(
            [df_orcamentaria, data.planilha_orcamentaria[is_seg].head(20)],
            ignore_index=True
        )

    data.store_test_df(df_name, df_orcamentaria)
    print('Generated test planilha orcamentaria!\n')


    print('Generating test planilha comprovacao...')
    # planilha comprovacao
    df_name = 'planilha_comprovacao'
    df_comprovacao = pd.DataFrame()
    for seg in data.planilha_comprovacao.idSegmento.unique():
        is_seg = data.planilha_comprovacao['idSegmento'] == seg
        df_comprovacao = pd.concat(
            [df_comprovacao, data.planilha_comprovacao[is_seg].head(20)],
            ignore_index=True
        )

    data.store_test_df(df_name, df_comprovacao)
    print('Generated test planilha comprovacao!\n')


    print('Generating test planilha captacao...')
    # planilha captacao
    df_name = 'planilha_captacao'
    df_captacao = pd.DataFrame()
    for p in data.planilha_captacao.Pronac.unique()[:2000]:
        is_p = data.planilha_captacao['Pronac'] == p
        df_captacao = pd.concat(
            [df_captacao, data.planilha_captacao[is_p].head(10)],
            ignore_index=True
        )

    data.store_test_df(df_name, df_captacao)
    print('Generated test planilha captacao!\n')
    

    print('Generating test planilha aprovacao comprovacao...')
    # planilha aprovacao comprovacao
    df_name = 'planilha_aprovacao_comprovacao'
    df_aprovacao_comprovacao = pd.DataFrame()
    for p in data.planilha_aprovacao_comprovacao.PRONAC.unique()[:2000]:
        is_p = data.planilha_aprovacao_comprovacao['PRONAC'] == p
        df_aprovacao_comprovacao = pd.concat(
            [df_aprovacao_comprovacao, data.planilha_aprovacao_comprovacao[is_p].head(10)],
            ignore_index=True
        )

    data.store_test_df(df_name, df_aprovacao_comprovacao)
    print('Generated test planilha aprovacao comprovacao!\n')
    
    data.store_test_df('planilha_projetos', data.planilha_projetos)

    print('Finished generation of test dataframes!')


@task
def test_metrics(ctx):
    """
    Train metrics with test dataframes.
    """
    raw_dir = './data/raw/'
    original = os.listdir(raw_dir)
    for fname in original:
        if '.pickle.gz' in fname:
            new_name = 'raw_' + fname
            src = raw_dir + fname
            dest = raw_dir + new_name
            os.rename(src, dest)

    try:
        manage(ctx, 'update_projects_metrics', env={})
    finally:
        for fname in os.listdir(raw_dir):
            if '.pickle.gz' in fname:
                new_name = fname.split('raw_')[1]
                src = raw_dir + fname
                dest = raw_dir + new_name
                os.rename(src, dest)


@task
def set_data(ctx, datatype='dev'):
    """
    Set dataframes for use.
    """
    data.clear()
    raw_dir = './data/raw/'
    dev_dir = './data/dev/'
    
    if datatype == 'dev':
        pop_raw(dev_dir)
        prepend_raw(raw_dir)
    
    elif datatype == 'prod':
        pop_raw(raw_dir)

    elif datatype == 'test':
        pop_raw(raw_dir)
        pop_raw(dev_dir)
        prepend_raw(raw_dir)
        prepend_raw(dev_dir)


@task
def test(ctx):
    ctx.run(
        'pytest -vv',
    )



@task(help={'c': 'command to be run with manage.py'})
def manager(ctx, c):
    """
    Runs commands that needs manage.py context
    Example of usage:
        $ inv manager createsuperuser
    """
    manage(ctx, c, env={})


def prepend_raw(data_dir):
    """
    Insert "raw_" to the begining of the file name of all files in data_dir.
    """
    for fname in os.listdir(data_dir):
        if 'raw_' not in fname and '.pickle.gz' in fname:
            new_name = 'raw_' + fname
            src = data_dir + fname
            dest = data_dir + new_name
            os.rename(src, dest)


def pop_raw(data_dir):
    """
    Remove "raw_" from the begining of the file name of all files in data_dir.
    """
    for fname in os.listdir(data_dir):
        if 'raw_' in fname and '.pickle.gz' in fname:
            new_name = fname[4:]
            src = data_dir + fname
            dest = data_dir + new_name
            os.rename(src, dest)
