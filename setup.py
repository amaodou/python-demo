#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

REQUIRED = [
    'requests>=2.20.0',
    'schedule==0.6.0'
]

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='python-demo',
    version='0.0.1',
    description='Demo of python',
    long_description=readme,
    author='amaodou',
    author_email='zzzzhyli@gmail.com',
    url='https://github.com/amaodou',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data = True,
    install_requires=REQUIRED,
    test_suite='nose.collector',
    tests_require=['nose'],
)
