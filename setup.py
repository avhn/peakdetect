#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

reqs = list()
with open('requirements.txt') as file:
    for line in file:
        line = line.strip()

        if line != '':
            reqs.append(line)

setup(
    name='peakdetect',
    version='1.0',
    description='Analytic peak finder',
    packages=['peakdetect'],
    url='https://github.com/Anaxilaus/peakdetect',
    author='Anaxilaus',
    install_requires=reqs
)
