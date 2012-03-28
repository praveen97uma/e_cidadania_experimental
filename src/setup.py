
import os
import re
from setuptools import setup, find_packages


setup(
    name = 'e-cidadania',
    description=("e-cidadania is a project to develop an open source "
		 "application for citizen participation, usable by "
		 "associations, companies and administrations."),
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
