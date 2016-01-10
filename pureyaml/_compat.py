# coding=utf-8
"""Python 2to3 compatibility handling."""
from __future__ import absolute_import

try:
    from logging import NullHandler
except ImportError:  # pragma: no cover
    import logging  # :off

    # Python < 2.7
    class NullHandler(logging.Handler):  # :on
        def emit(self, record):
            pass

try:
    from collections import abc as collections_abc
except ImportError:
    import collections  # :off

    # noinspection PyClassHasNoInit,PyPep8Naming
    class collections_abc:  # noqa
        Hashable = collections.Hashable  # :on
        Iterable = collections.Iterable
        Iterator = collections.Iterator
        Sized = collections.Sized
        Container = collections.Container
        Callable = collections.Callable
        Set = collections.Set
        MutableSet = collections.MutableSet
        Mapping = collections.Mapping
        MutableMapping = collections.MutableMapping
        MappingView = collections.MappingView
        KeysView = collections.KeysView
        ItemsView = collections.ItemsView
        ValuesView = collections.ValuesView
        Sequence = collections.Sequence
        MutableSequence = collections.MutableSequence

__all__ = ['NullHandler', 'collections_abc']
