from invoke import task
from src.salicml.data import csv_to_pickle


@task
def hello(ctx, name='world'):
    ctx.run(f'echo "hello {name}"')


@task
def pickle(ctx, clean=False):
    csv_to_pickle(clean=clean)