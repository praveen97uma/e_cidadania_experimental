
import os
import re
from setuptools import setup, find_packages


setup(
    name = 'e-cidadania',
    description=("The goal of this project is to create a framework for "
                 "representing Open Source contribution workflows, such as"
                 " the existing Google Summer of Code TM (GSoC) program."),
    version = 'UNKNOWN',
    packages = find_packages(exclude=['parts']),
    author='oscar',
    url='http://ecidadania.org',
    license='GPLv2',
    install_requires = [
        ],
    tests_require=[
        'django_nose',
        'nose',
	'webtest',
	'django_webtest',
        ],
    include_package_data = True,
    zip_safe = False,
    )
