#!/usr/bin/env python
# coding=utf-8
"""The full documentation is at https://pureyaml.readthedocs.org."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# TODO: put package requirements here
requirements = ['ply#bionikspoon/1.0.0', 'singledispatch']
# TODO: put package test requirements here
test_requirements = ['pytest', 'pytest-cov', 'future']
# TODO: put package setup requirements here
setup_requirements = ['pytest-runner', 'pytest-xdist', 'flake8']

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
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)  # :on
