#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

reqs = list()
with open('requirements.txt') as file:
    for line in file:
        line = line.strip()

        if line != '':
            reqs.append(line)

README = open('README.rst').read()
    
setup(
    name='peakdetect',
    version='1.1',
    description='Analytic peak finder',
    long_description=README,
    packages=['peakdetect'],
    url='https://github.com/Anaxilaus/peakdetect',
    author='Anaxilaus',
    install_requires=reqs
)
