#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

from .nodes import *  # noqa


def node_encoder(obj):  # noqa
    if isinstance(obj, dict):
        items = []
        for key, value in iteritems(obj):
            items.append((node_encoder(key), node_encoder(value)))
        return Map(*items)
    if isinstance(obj, list):
        items = []
        for item in obj:
            items.append(node_encoder(item))
        return Sequence(*items)
    if isinstance(obj, str):
        return Str(obj)
    if isinstance(obj, bool):
        return Bool(obj)
    if isinstance(obj, int):
        return Int(obj)
    if isinstance(obj, type(None)):
        return Null(obj)
    if isinstance(obj, float):
        return Float(obj)


class YAMLEncoder(NodeVisitor):
    def __init__(self, *args, **kwargs):
        pass

    def encode(self, obj):
        return ''.join(line for line in self.iterencode(obj))

    def iterencode(self, obj):
        nodes = node_encoder(obj)
        return self.visit(nodes)

    def visit_Sequence(self, node):
        for item in node:
            yield '- %s' % (yield item)

    def visit_Str(self, node):
        return node.value
