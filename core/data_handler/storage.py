import os
import pickle


def save(file_path, data):
    dirname_path = os.path.dirname(os.path.realpath(file_path))
    if not os.path.isdir(dirname_path):
        os.mkdir(dirname_path)

    with open(file_path, 'wb') as output_file:
        pickle.dump(data, output_file, pickle.DEFAULT_PROTOCOL)


def load(file_path, on_error_callback=None):
    try:
        with open(file_path, 'rb') as input_file:
            loaded_object = pickle.load(input_file)
            return loaded_object
    except FileNotFoundError:
        if on_error_callback:
            on_error_callback()
