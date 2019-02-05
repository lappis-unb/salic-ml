from setuptools import setup, find_packages

setup(
    name='salic-ml',
    version='0.1.0',
    description='Automate the Salic proposal admission process',
    url='https://github.com/lappis-unb/salic-ml',
    license='GPL v3.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'django~=2.1',
        'django-boogie',
        'django-cors-headers',
        'django-filter',
        'django-picklefield',
        'django-polymorphic',
        'django-pyodbc',
        'djangorestframework',
        'django-rest-swagger',
        'flask',
        'markdown',
        'numpy~=1.15.1',
        'pandas',
        'pyodbc',
        'psycopg2',
        'pymssql',
        'requests',
        'scikit-learn',
        'scipy',
        'pycpfcnpj',
    ],
    extras_require={
        'dev': [
            'click',
            'flake8',
            'invoke',
            'ipdb~=0.11',
            'ipython~=6.5.0',
            'jupyter',
            'matplotlib',
            'pytest~=3.8.0',
            'pytest-django',
            'seaborn~=0.9.0',
        ],
    },
    python_requires='>=3.5',
)
