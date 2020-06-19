# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in overtime_calculation/__init__.py
from overtime_calculation import __version__ as version

setup(
	name='overtime_calculation',
	version=version,
	description='Overtime Calculation',
	author='bizmap tech',
	author_email='suraj@bizmap.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
