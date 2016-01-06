#!/usr/bin/env python
# coding=utf-8
from collections import Mapping
from difflib import unified_diff

from pureyaml.nodes import Scalar, Collection, Node


def pformat_node(node, depth=0):  # noqa
    def indent():
        return '  ' * depth

    if isinstance(node, Scalar):
        yield indent() + str(Scalar)

    elif isinstance(node, Mapping):
        yield indent() + '<%s:(' % node.__class__.__name__
        depth += 1

        for k, v in node.items():
            depth += 1

            if isinstance(k, Scalar) and isinstance(v, Scalar):
                yield indent() + '%s, %s' % (k, v)
            else:
                yield indent() + ':'
                for line in pformat_node(k, depth=depth):
                    yield line

                yield indent() + '?'
                for line in pformat_node(v, depth=depth):
                    yield line

            depth -= 1

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
    if root is True:
        str_a = list(pformat_node(a))
        str_b = list(pformat_node(b))
        for line in unified_diff(str_a, str_b, n=2, lineterm=''):
            yield line
        yield ''

    if isinstance(a, Collection) and isinstance(b, Collection):
        for a_value, b_value in zip(a.value, b.value):
            if a_value == b_value:
                continue

            for line in get_node_diff(a_value, b_value, root=False):
                yield line
            break
    elif isinstance(a, tuple) and isinstance(b, tuple):
        (ak, av), (bk, bv) = a, b
        if not a == b:
            yield '(%s, %s) != (%s, %s)' % (ak, av, bk, bv)

    elif isinstance(a, (Node, tuple)) and isinstance(b, (Node, tuple)):
        yield '%s != %s' % (a, b)
    else:
        raise ValueError('%s != %s' % (a, b))
