import click

from salicml.middleware import Middleware


def train_all_metrics():
    print("Training all metrics")

    middleware = Middleware()
    middleware.train_all()


def train_number_of_items():
    print("Training number of items")

    middleware = Middleware()
    middleware.train_number_of_items()


@click.command()
@click.option("--train", type=click.Choice(["all", "number_of_items"]))
def main(train):
    if train:
        if train == "all":
            train_all_metrics()
        if train == "number_of_items":
            train_number_of_items()


if __name__ == "__main__":
    main()
