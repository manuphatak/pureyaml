#!/usr/bin/env python
# coding=utf-8
"""The full documentation is at https://pureyaml.readthedocs.org."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.pytest_args += ' --cov=pureyaml'

    def run_tests(self):
        import pytest
        import sys

        print(self.pytest_args)
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['ply#3.8+bionikspoon', 'future']
dependency_links = []
test_requirements = ['pytest', 'pytest-cov', 'pytest-xdist', 'future', 'pyyaml']
setup_requirements = ['flake8', 'ply#3.8+bionikspoon', 'future']

setup(  # :off
    name='pureyaml',
    version='0.1.0',
    description='Yet another yaml parser, in pure python.',
    long_description='\n\n'.join([readme, history]),
    author='Manu Phatak',
    author_email='bionikspoon@gmail.com',
    url='https://github.com/bionikspoon/pureyaml',
    packages=['pureyaml', 'pureyaml.grammar'],
    package_dir={'pureyaml': 'pureyaml'},
    include_package_data=True,
    license='MIT',
    zip_safe=False,
    keywords='pureyaml Manu Phatak',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: YACC',
        'Topic :: Database',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Internet',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities',
    ],
    test_suite='tests',
    cmdclass={'test': PyTest},
    install_requires=requirements,
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    dependency_links=dependency_links
)  # :on
