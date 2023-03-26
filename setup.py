#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open("README.md", "r", encoding="UTF-8") as f:
    readme = f.read()

with open("requirements.txt", "r", encoding="UTF-8") as f:
    requirements = f.read().splitlines()

setup(
    name='rna_map_tools',
    version='0.1.0',
    description='a set of tools for organizing more complex analysis and processing of rna map data',
    long_description=readme,
    long_description_content_type="test/markdown",
    author='Joe Yesselman',
    author_email='jyesselm@unl.edu',
    url='https://github.com/jyesselm/rna_map_tools',
    packages=[
        'rna_map_tools',
    ],
    package_dir={'rna_map_tools': 'rna_map_tools'},
    py_modules=[
        'rna_map_tools/cli'
    ],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='rna_map_tools',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    entry_points = {
        'console_scripts' : [
            'rna-map-tools = rna_map_tools.cli:cli'
        ]
    }
)
