#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from collections import namedtuple
from difflib import get_close_matches

try:
    from collections import OrderedDict
except ImportError:
    from future.moves.collections import OrderedDict

from future.utils import with_metaclass, iteritems


class OrderedTestMeta(type):
    def __new__(cls, cls_name, bases, cls_dict):  # noqa
        d = dict(cls_dict)
        _data = namedtuple(cls_name, ['data', 'expected'])
        order = []

        for name, value in iteritems(cls_dict):
            # Guard, internal api attributes
            if not name.startswith('test_'):
                continue

            # setup
            is_data = name.endswith('__data')
            is_expected = name.endswith('__expected')

            # Guard, deal with the easy case.
            is_simple_definition = not is_data and not is_expected
            if is_simple_definition:
                if len(value) != 2:
                    msg = '%r in class %r improperly configured.\n!! Expecting a 2-tuple, got: %r'
                    raise AttributeError(msg % (name, cls_name, value))
                # Add onto ordered list.
                d[name] = _data(*value)
                order.append(name)
                continue

            _name = name
            # rename attribute: strip suffix
            if is_data:
                name = name[:-len('__data')]
            if is_expected:
                name = name[:-len('__expected')]

            # remove original attributes from dict
            data = d.pop(name + '__data', None)
            expected = d.pop(name + '__expected', None)

            # Guard, improperly defined attribute or second visit
            if not data or not expected:
                # second visit
                if name in order:
                    continue

                # error handling
                if data:
                    missing_attr = name + '__expected'
                elif expected:
                    missing_attr = name + '__data'
                else:
                    missing_attr = 'Unknown'

                choices = [key for key in cls_dict if key != _name]
                close_match = get_close_matches(missing_attr, choices, 1)
                if close_match:
                    misspelled = '\n\nDid you mistype  %r  ?' % close_match[0]
                else:
                    misspelled = ''

                msg = '%r in class %r improperly configured.\n!! Missing attribute: %r%s'
                raise AttributeError(msg % (name, cls_name, missing_attr, misspelled))

            # Add onto ordered list.
            d[name] = _data(data, expected)
            order.append(name)

        d['__ordered__'] = order
        return type.__new__(cls, cls_name, bases, d)

    @classmethod
    def __prepare__(*_):
        return OrderedDict()


class ParametrizedTestData(with_metaclass(OrderedTestMeta)):
    @classmethod
    def keys(cls):
        return cls.__ordered__

    @classmethod
    def get(cls, item):
        return cls.__dict__[item]
