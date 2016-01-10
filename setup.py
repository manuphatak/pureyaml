#!/usr/bin/env python
# coding=utf-8
"""The full documentation is at https://pureyaml.readthedocs.org."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        import sys

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# TODO: put package requirements here
requirements = ['ply', 'singledispatch']
dependency_links = ['git+git://github.com/bionikspoon/ply.git@1.0.0#egg=ply']
# TODO: put package test requirements here
test_requirements = ['pytest', 'future']

# TODO: put package setup requirements here
setup_requirements = ['flake8']

setup(  # :off
    name='pureyaml',
    version='0.1.0',
    description='Yet another yaml parser, in pure python.',
    long_description='\n\n'.join([readme, history]),
    author='Manu Phatak',
    author_email='bionikspoon@gmail.com',
    url='https://github.com/bionikspoon/pureyaml',
    packages=['pureyaml'],
    package_dir={'pureyaml': 'pureyaml'},
    include_package_data=True,
    license='MIT',
    zip_safe=False,
    cmdclass={'test': PyTest},
    keywords='pureyaml Manu Phatak',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='tests',
    install_requires=requirements,
    dependency_links=dependency_links,
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)  # :on
