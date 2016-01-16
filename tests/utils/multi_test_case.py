#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from collections import namedtuple
from difflib import get_close_matches

from tests.utils import PY34, PY35, PY33

try:
    from collections import OrderedDict, defaultdict
except ImportError:
    from future.moves.collections import OrderedDict, defaultdict

from future.utils import with_metaclass, iteritems, PY26, PY27, PYPY


def head_and_tail(x, *xs):
    if not xs:
        raise ValueError('{0} is missing metadata tags'.format(x))
    return x, xs


def separate_version_tags(meta):
    _meta = []
    _versions = []
    for tag in meta:
        if 'PY' in tag:
            _versions.append(tag)
        else:
            _meta.append(tag)
    return tuple(_versions), tuple(_meta)


def separate_action_tags(meta):
    ACTION_INDICATOR = 'test_'
    _meta = []
    _actions = []
    for tag in meta:
        if tag.startswith(ACTION_INDICATOR):
            action = tag[len(ACTION_INDICATOR):]
            _actions.append(action)
        else:
            _meta.append(tag)
    return tuple(_actions), tuple(_meta)


map_version = {  # :off
    'PY26': PY26,
    'PY27': PY27,
    'PY33': PY33,
    'PY34': PY34,
    'PY35': PY35,
    'PYPY': PYPY,
    'not_PY26': not PY26,
    'not_PY27': not PY27,
    'not_PY33': not PY33,
    'not_PY34': not PY34,
    'not_PY35': not PY35,
    'not_PYPY': not PYPY,
}  # :on


def is_correct_python_version(version_tags):
    # Guard, no specific version tag specified
    if not version_tags:
        return True

    return all(map(lambda tag: map_version[tag], version_tags))


class MultiTestMeta(type):
    def __new__(cls, cls_name, bases, cls_dict):  # noqa
        d = defaultdict(dict)
        d.update(dict(cls_dict))
        _data = namedtuple(cls_name, ['data', 'expected'])
        order = defaultdict(list)

        test_q = {}

        for name, value in iteritems(cls_dict):
            # Guard, skip internal object attributes
            if not name.startswith('it_'):
                continue

            test_name, meta = head_and_tail(*name.split('__'))

            # Guard, store test data, and move on.
            if 'data' in meta:
                test_q[test_name] = value
                continue

            # Guard, expectations defined before data (simplicity)
            test_data = test_q.get(test_name, None)
            if test_data is None:
                # TODO detailed error message
                raise AttributeError('missing test data')

            # Guard, skip specs for other versions of python
            version_meta_tags, meta = separate_version_tags(meta)
            if not is_correct_python_version(version_meta_tags):
                continue

            # Guard, missing meta data
            action_meta_tags, meta = separate_action_tags(meta)
            if not action_meta_tags:
                # TODO detailed error message
                raise AttributeError('missing meta tags')

            # add test to class
            for action in action_meta_tags:

                d[action][test_name] = _data(test_data, value)
                order[action].append(test_name)

            # # setup
            # is_data = name.endswith('__data')
            # is_expected = name.endswith('__expected')
            #
            # # Guard, deal with the easy case.
            # is_simple_definition = not is_data and not is_expected
            # if is_simple_definition:
            #     if len(value) != 2:
            #         msg = '%r in class %r improperly configured.\n!! Expecting a 2-tuple, got: %r'
            #         raise AttributeError(msg % (name, cls_name, value))
            #     # Add onto ordered list.
            #     d[name] = _data(*value)
            #     order.append(name)
            #     continue
            #
            # _name = name
            # # rename attribute: strip suffix
            # if is_data:
            #     name = name[:-len('__data')]
            # if is_expected:
            #     name = name[:-len('__expected')]
            #
            # # remove original attributes from dict
            # data = d.pop(name + '__data', None)
            # expected = d.pop(name + '__expected', None)
            #
            # # Guard, improperly defined attribute or second visit
            # if not data or not expected:
            #     # second visit
            #     if name in order:
            #         continue
            #
            #     # error handling
            #     if data:
            #         missing_attr = name + '__expected'
            #     elif expected:
            #         missing_attr = name + '__data'
            #     else:
            #         missing_attr = 'Unknown'
            #
            #     choices = [key for key in cls_dict if key != _name]
            #     close_match = get_close_matches(missing_attr, choices, 1)
            #     if close_match:
            #         misspelled = '\n\nDid you mistype  %r  ?' % close_match[0]
            #     else:
            #         misspelled = ''
            #
            #     msg = '%r in class %r improperly configured.\n!! Missing attribute: %r%s'
            #     raise AttributeError(msg % (name, cls_name, missing_attr, misspelled))
            #
            # # Add onto ordered list.
            # d[name] = _data(data, expected)
            # order.append(name)

        d['__ordered__'] = order
        return type.__new__(cls, cls_name, bases, d)

    @classmethod
    def __prepare__(*_):
        return OrderedDict()


class MultiTestCaseBase(with_metaclass(MultiTestMeta)):
    @classmethod
    def keys(cls, category):
        return cls.__ordered__[category]

    @classmethod
    def get(cls, category, item):
        return cls.__dict__[category][item]
