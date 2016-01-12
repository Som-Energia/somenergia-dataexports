#!/usr/bin/python
from setuptools import setup
import os

def localfile(file):
    currentDir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(currentDir,file)

from pip.req import parse_requirements

with open(localfile('README.rst')) as readmefile:
    readme = readmefile.read()

setup(
    name = "somenergia-dataexports",
    version = "0.1",
    description = "Scripts to export data and reports from SomEnergia ERP",
    author = "SomEnergia",
    author_email = "tic@somenergia.coop",
    url = 'https://github.com/Som-Energia/somenergia-dataexports',
    long_description = readme,
    license = 'GNU General Public License v3 or later (GPLv3+)',
    py_modules=[
        'sql2csv',
    ],
    scripts=[
        'mapa_socis',
        'distribucio_de_socies',
        'mchimp_generationsocis.py',
    ],
    install_requires=[
        str(req.req)
        for req in parse_requirements(localfile('requirements.txt'))
    ],
    test_suite='nose2.collector.collector',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
)

