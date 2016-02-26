#!/usr/bin/env python


"""
Setup script for bqapi
"""


import os

from setuptools import find_packages
from setuptools import setup


with open('README.rst') as f:
    readme = f.read().strip()


def parse_dunder_line(string):

    """
    Take a line like:

        "__version__ = '0.0.8'"

    and turn it into a tuple:

        ('__version__', '0.0.8')

    Not very fault tolerant.
    """

    # Split the line and remove outside quotes
    variable, value = (s.strip() for s in string.split('=')[:2])
    value = value[1:-1].strip()
    return variable, value


with open(os.path.join('bqapi', '__init__.py')) as f:
    dunders = dict((
        parse_dunder_line(line) for line in f if line.strip().startswith('__')))
    version = dunders['__version__']
    author = dunders['__author__']
    email = dunders['__email__']
    source = dunders['__source__']


setup(
    name='bqapi',
    author=author,
    author_email=email,
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    description="Experimental BigQuery interface for Python",
    include_package_data=True,
    install_requires=[
        'oauth2client',
        'google-api-python-client'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'coveralls',
        ],
    },
    keywords='BigQuery Python DBAPI 2.0',
    license="Apache 2.0",
    long_description=readme,
    packages=find_packages(exclude=['tests']),
    url=source,
    version=version,
    zip_safe=True
)
