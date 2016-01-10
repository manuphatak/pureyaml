#!/usr/bin/env python
# coding=utf-8
import os
from collections import Mapping, namedtuple, OrderedDict
from difflib import Differ, unified_diff, get_close_matches

from pureyaml.nodes import Scalar, Collection, Node, Docs


def test_dir(*paths):
    dirname = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(dirname, *paths))


def pformat_node(node, depth=0):  # noqa
    __tracebackhide__ = True

    def indent():
        return '  ' * depth

    if isinstance(node, Scalar):
        yield indent() + str(node)

    elif isinstance(node, Mapping):
        yield indent() + '<%s:(' % node.__class__.__name__
        depth += 1

        for k, v in node.items():

            if isinstance(k, Scalar) and isinstance(v, Scalar):
                depth += 1
                yield indent() + '%s, %s' % (k, v)
                depth -= 1
            else:

                lines = pformat_node(k, depth=depth + 1)
                yield indent() + '? ' + next(lines).strip(' ')

                for line in lines:
                    yield line

                lines = pformat_node(v, depth=depth + 1)
                yield indent() + ': ' + next(lines).strip(' ')
                for line in lines:
                    yield line

        depth -= 1
        yield indent() + ')>'

    elif isinstance(node, Collection):
        yield indent() + '<%s:(' % node.__class__.__name__
        depth += 1
        for value in node.value:
            if not isinstance(value, Node) or not value.value:
                continue
            for line in pformat_node(value, depth=depth):
                yield line
        depth -= 1
        yield indent() + ')>'


def get_node_diff(a, b, root=True):  # noqa
    __tracebackhide__ = True

    d = Differ()
    if root is True:
        str_a = list(pformat_node(a))
        str_b = list(pformat_node(b))
        for line in unified_diff(str_a, str_b, n=2, lineterm=''):
            yield line
        yield ''
        yield '%s != %s' % (a, b)
        yield ''

    if isinstance(a, Collection) and isinstance(b, Collection):
        for a_value, b_value in zip(a.value, b.value):
            if a_value == b_value:
                continue

            for line in get_node_diff(a_value, b_value, root=False):
                yield line
            break
    elif isinstance(a, tuple) and isinstance(b, tuple):
        # (ak, av), (bk, bv) = a, b
        if not a == b:
            for line in d.compare([repr(a)], [repr(b)]):
                yield line.rstrip('\n')
                # yield '(%s, %s) != (%s, %s)' % (ak, av, bk, bv)

    elif isinstance(a, (Node, tuple)) and isinstance(b, (Node, tuple)):
        for line in d.compare([repr(a)], [repr(b)]):
            yield line.rstrip('\n')
    else:
        raise ValueError('%s != %s' % (a, b))


# TODO delete this
def _serialize_nodes(node, depth=0):  # noqa
    __tracebackhide__ = True

    def indent():
        return '    ' * depth

    if isinstance(node, Scalar):
        yield indent() + '%s(%r)' % (node.__class__.__name__, node.value)

    elif isinstance(node, Mapping):
        yield indent() + '%s(' % node.__class__.__name__
        depth += 1

        for k, v in node.items():

            if isinstance(k, Scalar) and isinstance(v, Scalar):
                k_value = next(_serialize_nodes(k))
                v_value = next(_serialize_nodes(v))
                yield indent() + '(%s, %s),' % (k_value, v_value)
            elif isinstance(k, Scalar):
                yield indent() + '('
                depth += 1
                for line in _serialize_nodes(k):
                    yield indent() + line
                for line in _serialize_nodes(v):
                    yield indent() + line
                depth -= 1
                yield indent() + '),'

        depth -= 1
        yield indent() + ')'

    elif isinstance(node, Collection):
        off = '  # :off' if isinstance(node, Docs) else ''
        on = '  # :on' if isinstance(node, Docs) else ''
        var = 'expected = ' if isinstance(node, Docs) else ''
        if isinstance(node, Docs):
            yield ''
        yield indent() + '%s%s(%s' % (var, node.__class__.__name__, off)
        depth += 1
        if isinstance(node, Docs):
            depth += 1
        for value in node.value:
            if not isinstance(value, Node) or not value.value:
                continue
            for line in _serialize_nodes(value, depth=depth):
                if line.endswith(')'):
                    yield line + ','
                else:
                    yield line
        depth -= 1
        yield indent() + ')%s' % on


def serialize_nodes(nodes):
    return '\n'.join(_serialize_nodes(nodes))


class OrderedTestMeta(type):
    def __new__(cls, cls_name, bases, cls_dict):  # noqa
        d = dict(cls_dict)
        _data = namedtuple(cls_name, ['data', 'expected'])
        order = []
        for name, value in cls_dict.items():
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

                choices = [key for key in cls_dict.keys() if key != _name]
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


class ParametrizedTestData(metaclass=OrderedTestMeta):
    @classmethod
    def keys(cls):
        return cls.__ordered__

    @classmethod
    def get(cls, item):
        return cls.__dict__[item]
