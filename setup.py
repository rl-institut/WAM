#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    dependencies = {
        requirement
        for requirement in requirements
        if requirement.startswith('git')
    }
    requirements = set(requirements) - dependencies

setup(
    name='wam',
    version='1.0',
    packages=find_packages(),
    install_requires=requirements,
    dependency_links=dependencies,
    scripts=['manage.py']
)
