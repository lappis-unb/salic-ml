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
        'django',
        'flask',
        'numpy~=1.15.1',
        'pandas~=0.23.4',
        'pyodbc',
        'requests',
        'scikit-learn',
        'scipy',
        'tables',
        'pycpfcnpj',
    ],
    extras_require={
        'dev': [
            'click',
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
    python_requires='>=3.6',
)
