# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='CouchDB',
    version='0.0.1',
    description='Library for CouchDB',
    long_description=readme,
    author='Mohamed Hashi',
    author_email='maxamedhashi@gmail.com',
    url='https://github.com/mqrzy/couchdb.py',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
