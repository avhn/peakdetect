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
    version='1.2',
    description='Simple peak detection',
    long_description=README,
    packages=['peakdetect'],
    url='https://github.com/avhn/peakdetect',
    author='avhn',
    install_requires=reqs
)
