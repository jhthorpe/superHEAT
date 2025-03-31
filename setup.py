# setup.py
#
#   March 28, 2025 @ ANL : JHT added
#
# setup for installing this repo via pip

import sys
import os
from setuptools import setup
from setuptools import find_packages


setup(
    name='superHEAT',
    version=0.1,
    author='James H. Thorpe',
    author_email='james.thorpe@utexas.edu',
    description='Supports the generation, curation, and analysis of theoretical model chemistries',
    license='GPL-3.0',
    long_description=open('README.md').read(),
    packages=find_packages(),
    python_requires='>=3.0'
)
