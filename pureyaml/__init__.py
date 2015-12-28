#!/usr/bin/env python
# coding=utf-8
"""
==============
pureyaml
==============

Yet another yaml parser, in pure python.

"""
from __future__ import absolute_import
import logging

from ._compat import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

__author__ = 'Manu Phatak'
__email__ = 'bionikspoon@gmail.com'
__version__ = '0.1.0'
