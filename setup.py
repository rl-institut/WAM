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
    version='0.1.3',
    packages=find_packages(),
    license='GNU Affero General Public License v3.0',
    author='henhuy, nesnoj, Bachibouzouk, christian-rli, 4lm',
    description='WAM - Web Applications & Maps',
    url='https://github.com/rl-institut/WAM',
    install_requires=normal_requirements + git_requirements,
    scripts=['manage.py']
)
