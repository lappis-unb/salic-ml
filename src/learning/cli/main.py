import click

from learning.middleware import Middleware


def train_all_metrics():
    print("Training all metrics")

    middleware = Middleware()
    middleware.train_all()


def train_number_of_items():
    print("Training number of items")

    middleware = Middleware()
    middleware.train_number_of_items()


def train_metrics(train):
    if train:
        if train == "all":
            train_all_metrics()
        if train == "number_of_items":
            train_number_of_items()
