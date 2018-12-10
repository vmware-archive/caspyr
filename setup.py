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
	name='cassdk',
	version='0.0.1',  # placeholder
	url='https://github.com/grantorchard/caspyr',
	license='',
	author='Grant Orchard',
	author_email='',
	description='A python project for VMware Cloud Automation Services.',
	long_description=long_description,
	install_requires=['requests[security] == 2.20.0'],

	classifiers=[
		'Intended Audience :: Developers',
		'Development Status :: 3 - Alpha',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],
	project_urls={
		'Source': 'https://github.com/grantorchard/caspyr',
	},
	platforms=["python_version >= '3.6'", "python_version <= '3.7'"]
)
