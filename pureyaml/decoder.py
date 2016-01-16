#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

from .nodes import NodeVisitor
from .parser import YAMLParser


# noinspection PyMethodMayBeStatic
class YAMLDecoder(NodeVisitor):
    def decode(self, s):
        return self.visit(YAMLParser().parse(s))

    def visit_Docs(self, node):
        for doc in node.value:
            yield (yield doc)

    def visit_Sequence(self, node):
        sequence = []
        for item in node.value:
            sequence.append((yield item))
        yield sequence

    def visit_Map(self, node):
        map = {}
        for key, value in node.value:
            map[(yield key)] = (yield value)
        yield map

    def visit_Scalar(self, node):
        return node.type(node.value)

    def visit_Null(self, _):
        return None
    visit_Doc = visit_Docs
    visit_Str = visit_Scalar
    visit_Int = visit_Scalar
    visit_Float = visit_Scalar
    visit_Bool = visit_Scalar

    def visit_Binary(self, node):
        return node.value
