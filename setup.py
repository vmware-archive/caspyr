# Copyright 2018-2019 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from setuptools import setup

CURRENT_PYTHON = sys.version_info[:2]
MIN_REQUIRED_PYTHON = (3, 6)
MAX_REQUIRED_PYTHON = (3, 7)

if not MIN_REQUIRED_PYTHON <= CURRENT_PYTHON <= MAX_REQUIRED_PYTHON:
    sys.stderr.write(
        """
        ==========================
        Unsupported Python version
        ==========================
        """
    )

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='caspyr',
    version='0.0.1',  # placeholder
    url='https://github.com/vmware/caspyr',
    license='Apache v2',
    author='Grant Orchard',
    author_email='gorchard@vmware.com',
    description='A python project for VMware Cloud Automation Services.',
    long_description=long_description,
    packages=['caspyr'],
    install_requires=['requests'],

    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        'Source': 'https://github.com/vmware/caspyr',
    },
    platforms=["python_version >= '3.6'", "python_version <= '3.7'"]
)
