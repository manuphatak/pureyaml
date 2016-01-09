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
from .decoder import YAMLDecoder

logging.getLogger(__name__).addHandler(NullHandler())

__author__ = 'Manu Phatak'
__email__ = 'bionikspoon@gmail.com'
__version__ = '0.1.0'


def load(s, **kwargs):
    return loads(s, **kwargs)


def loads(s, cls=None, **kw):
    if not isinstance(s, str):
        raise TypeError('the YAML object must be str, not {!r}'.format(s.__class__.__name__))

    cls = cls or YAMLDecoder
    return cls(**kw).decode(s)
