from setuptools import setup, find_packages

setup(
    name='salic-ml',
    version='0.0.6',
    description='Automate the Salic proposal admission process',
    url='https://github.com/lappis-unb/salic-ml',
    license='GPL v3.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'click', 'jupyter', 'matplotlib', 'numpy', 'pandas', 'requests',
        'scikit-learn', 'scipy'
    ],
    python_requires='>=3',
)
