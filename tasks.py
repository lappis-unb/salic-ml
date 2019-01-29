from invoke import task
from src.salicml.data import csv_to_pickle
from src.learning.cli import train_metrics as train


@task
def hello(ctx, name='world'):
    ctx.run(f'echo "hello {name}"')


@task
def pickle(ctx, clean=False):
    csv_to_pickle(clean=clean)


@task
def train_metrics(ctx, train_type='all'):
    """
    Trains the projects financial indicator metrics, using db information

    """
    train(train_type)


@task
def update_db(ctx, update_pickle=True):
    """
    Updates local django db projects and pickle files using salic database from
    MinC
    """
    return None
