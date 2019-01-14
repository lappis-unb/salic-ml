from invoke import task
from src.salicml.data import csv_to_pickle
from src.learning.cli import train_metrics


@task
def hello(ctx, name='world'):
    ctx.run(f'echo "hello {name}"')


@task
def pickle(ctx, clean=False):
    csv_to_pickle(clean=clean)


@task
def train_metrics(ctx, train_type='all'):
    """
    Trains the models for implemented feature-middlewares in learning. It will
    try to load the stored training models.

    type can be all or  number_of_items
    """
    train_metrics(train_type)
