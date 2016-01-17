#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from collections import Mapping

from pureyaml.nodes import Scalar, Collection, Node, Docs


def serialize_nodes(nodes):
    return '\n'.join(_serialize_nodes(nodes))


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
                    yield indent() + line + ','
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
