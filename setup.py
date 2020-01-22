# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='trains',
    version='0.0.1',
    description='ThoughtWorks "Trains" assignment',
    long_description=readme,
    author='Frank Carnovale',
    author_email='frank.carnovale@gmail.com',
    url='https://github.com/frank-carnovale/trains',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

