import sys
import click
import requests


@click.command()
@click.argument('url')
@click.argument('filename', type=click.Path())
def download_file(url, filename):
    print('Downloading from {} to {}'.format(url, filename))

    response = requests.get(url, stream = True)
    file_size = int(response.headers.get('content-length'))

    with open(filename, 'wb') as output_file:
        data_loaded = 0

        for data in response.iter_content(chunk_size = 4096):
            data_loaded += len(data)
            output_file.write(data)

            progress = int(50 * data_loaded / file_size)
            fill_progress = '=' * progress
            empty_progress = ' ' * (50 - progress)
            percentage_progress = (data_loaded * 100 / file_size)

            message = "\r[%s%s] %d%% / 100%%" % (fill_progress, empty_progress,
                                                 percentage_progress)

            sys.stdout.write(message)
            sys.stdout.flush()


if __name__ == '__main__':
    download_file()
