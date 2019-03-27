from invoke import task
import os
import sys

from src.salicml.data import csv_to_pickle
from src.salicml.data.db_operations import save_sql_to_files, save_sql_to_file
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


@task(help={'models': "Default is True, updates api models",
            'pickles': "Default is False, save queries in pickles",
            'f': "Default is False, force to save files even if already exists"})
def update_data(ctx, models=True, pickles=False, f=False):
    """
    Updates local django db projects and pickle files using salic database from
    MinC
    Pickles are saved in /data/raw/ from sql queries in /data/scripts/
    Models are created from /data/scripts/models/
    """
    if pickles:
        save_sql_to_files(f)
    if models:
        if f:
            manage(ctx, 'create_models_from_sql --force True', env={})
        else:
            manage(ctx, 'create_models_from_sql', env={})


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


@task(help={'c': 'command to be run with manage.py'})
def manager(ctx, c):
    """
    Runs commands that needs manage.py context
    Example of usage:
        $ inv manager createsuperuser
    """
    manage(ctx, c, env={})
