#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    dependencies = [req for req in requirements if req.startswith('git')]
    requirements = list(set(requirements) - set(dependencies))

setup(
    name='wam',
    version='1.0',
    packages=find_packages(),
    install_requires=requirements,
    dependency_links=dependencies,
    scripts=['manage.py']
)
