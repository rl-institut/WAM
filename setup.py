#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    git_requirements = [
        f"{req.split('#egg=')[1]} @ {req}"
        for req in requirements if req.startswith('git')
    ]
    normal_requirements = [req for req in requirements if not req.startswith('git')]

setup(
    name='wam',
    version='1.0',
    packages=find_packages(),
    install_requires=normal_requirements + git_requirements,
    scripts=['manage.py']
)
