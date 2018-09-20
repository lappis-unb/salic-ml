#!/usr/bin/env python

# Dependencies
#
## Packages
### pip install --upgrade setuptools wheel twine
#
## Run
### PIP_USER="" PIP_PASSWORD="" python update_pip.py


import os
import re
import sys
import requests


FILE_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT_PATH = FILE_PATH
SETUP_PATH = os.path.join(FILE_PATH, 'setup.py')
DIST_FOLDER_PATH = os.path.join(FILE_PATH, 'dist')

PIP_USER = os.environ.get('PIP_USER', '')
PIP_PASSWORD = os.environ.get('PIP_PASSWORD', '')

BUILD_COMMAND = 'python setup.py bdist_wheel --universal'
PIP_PUSH_COMMAND = 'twine upload -u {0} -p "{1}" --repository-url https://upload.pypi.org/legacy/ dist/*'.format(PIP_USER, PIP_PASSWORD)
REMOVE_OLD_BUILD_COMMAND = 'rm -rf dist/ *.egg-info'


with open(SETUP_PATH, 'r') as ofile:
    file_content = ofile.read()
    salicml_version = re.search(r"^.+version='(.+)'", file_content, re.MULTILINE).groups()[0]


url = "https://pypi.org/pypi/salic-ml/json"
response = requests.get(url=url)

pip_salicml_version = response.json()['info']['version']

if salicml_version == pip_salicml_version:
    print("This version is already updated in pip")
    exit()

os.system("cd {}; {}".format(PROJECT_ROOT_PATH, REMOVE_OLD_BUILD_COMMAND))
os.system("cd {}; {}".format(PROJECT_ROOT_PATH, BUILD_COMMAND))
os.system("cd {}; {}".format(PROJECT_ROOT_PATH, PIP_PUSH_COMMAND))

print("salic-ml {} updated on pip".format(salicml_version))
