#!/usr/bin/env python
# coding=utf-8
import os
from collections import Mapping
from difflib import *

from pureyaml.nodes import Scalar, Collection, Node, Docs


def test_dir(*paths):
    dirname = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(dirname, *paths))


def pformat_node(node, depth=0):  # noqa
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

                lines = pformat_node(k, depth=depth+1)
                yield indent() + '? ' + next(lines).strip(' ')

                for line in lines:
                    yield line

                lines = pformat_node(v, depth=depth+1)
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


# TODO delete this
def _serialize_nodes(node, depth=0):  # noqa
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
