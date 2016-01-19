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


def dump(obj, fp=None, indent=None, sort_keys=False, **kw):
    """
    Dump object to a file like object or string.

    :param obj:
    :param fp: Open file like object
    :param int indent: Indent size, default 2
    :param bool sort_keys: Optionally sort dictionary keys.
    :return: Yaml serialized data.
    """

    if fp:
        iterable = YAMLEncoder(indent=indent, sort_keys=sort_keys, **kw).iterencode(obj)
        for chunk in iterable:
            fp.write(chunk)
    else:
        return dumps(obj, indent=indent, sort_keys=sort_keys, **kw)


def dumps(obj, indent=None, default=None, sort_keys=False, **kw):
    """Dump string."""
    return YAMLEncoder(indent=indent, default=default, sort_keys=sort_keys, **kw).encode(obj)


def load(s, **kwargs):
    """Load yaml file"""
    try:
        return loads(s, **kwargs)
    except TypeError:
        return loads(s.read(), **kwargs)


def loads(s, cls=None, **kwargs):
    """Load string"""
    if not isinstance(s, string_types):
        raise TypeError('the YAML object must be str, not {0!r}'.format(s.__class__.__name__))

    cls = cls or YAMLDecoder
    return cls(**kwargs).decode(s)
