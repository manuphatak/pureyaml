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

from future.utils import string_types

from ._compat import NullHandler
from .decoder import YAMLDecoder
from .encoder import YAMLEncoder

logging.getLogger(__name__).addHandler(NullHandler())

__author__ = 'Manu Phatak'
__email__ = 'bionikspoon@gmail.com'
__version__ = '0.1.0'


def dump(obj, fp=None, cls=None, indent=None, sort_keys=False, **kw):
    cls = cls or YAMLEncoder
    if fp:
        iterable = cls(indent=indent, sort_keys=sort_keys, **kw).iterencode(obj)
        for chunk in iterable:
            fp.write(chunk)
    else:
        return dumps(obj, cls=cls, indent=indent, sort_keys=sort_keys, **kw)


def dumps(obj, cls=None, indent=None, default=None, sort_keys=False, **kw):
    cls = cls or YAMLEncoder
    return cls(indent=indent, default=default, sort_keys=sort_keys, **kw).encode(obj)


def load(s, **kwargs):
    try:
        return loads(s, **kwargs)
    except TypeError:
        return loads(s.read(), **kwargs)


def loads(s, cls=None, **kwargs):
    if not isinstance(s, string_types):
        raise TypeError('the YAML object must be str, not {!r}'.format(s.__class__.__name__))

    cls = cls or YAMLDecoder
    return cls(**kwargs).decode(s)
