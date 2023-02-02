from setuptools import setup

setup(
    name='scbapi',
    version='0.0.1',
    description='Funktion för anrop av SCPs API',
    author='oj',
    license='BSD 2-clause',
    packages=['scbapi'],
    install_requires=[
        'requests>=2.27.1',
        'pandas>=1.3.3'
    ],
)

