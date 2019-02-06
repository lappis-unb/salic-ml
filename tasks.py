from invoke import task
from src.salicml.data import csv_to_pickle
from src.salicml.data.db_operations import save_sql_to_files


@task
def hello(ctx, name='world'):
    ctx.run(f'echo "hello {name}"')


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
    ctx.run('python3 manage.py update_projects_metrics')


@task
def update_db(ctx, update_models=True, update_pickle=True):
    """
    Updates local django db projects and pickle files using salic database from
    MinC
    """
    if update_pickle:
        save_sql_to_files()
    if update_models:
        ctx.run('python3 manage.py create_models_from_sql')
