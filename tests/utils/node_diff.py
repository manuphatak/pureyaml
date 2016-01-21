#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from difflib import Differ, unified_diff

from pureyaml.nodes import Collection, Node
from tests.utils.serialize_nodes import serialize_nodes


def get_node_diff(a, b, root=True):  # noqa

    d = Differ()
    if root is True:
        str_a = serialize_nodes(a, paste_friendly=False).splitlines()
        str_b = serialize_nodes(b, paste_friendly=False).splitlines()
        for line in unified_diff(str_a, str_b, n=10, lineterm=''):
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
            for line in d.compare(serialize_nodes(a, paste_friendly=False).splitlines(),
                                  serialize_nodes(b, paste_friendly=False).splitlines()):
                yield line.rstrip('\n')
                # yield '(%s, %s) != (%s, %s)' % (ak, av, bk, bv)

    elif isinstance(a, (Node, tuple)) and isinstance(b, (Node, tuple)):
        for line in d.compare(serialize_nodes(a, paste_friendly=False).splitlines(),
                              serialize_nodes(b, paste_friendly=False).splitlines()):
            yield line.rstrip('\n')
    else:
        raise ValueError('%s != %s' % (a, b))
