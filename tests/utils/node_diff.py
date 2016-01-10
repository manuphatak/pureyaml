#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from collections import Mapping
from difflib import Differ, unified_diff

from future.utils import iteritems

from pureyaml.nodes import Scalar, Collection, Node


def pformat_node(node, depth=0):  # noqa

    def indent():
        return '  ' * depth

    if isinstance(node, Scalar):
        yield indent() + str(node)

    elif isinstance(node, Mapping):
        yield indent() + '<%s:(' % node.__class__.__name__
        depth += 1

        for k, v in iteritems(node):

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
