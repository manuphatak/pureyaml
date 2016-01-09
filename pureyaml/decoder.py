#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

from .parser import YAMLParser
from .nodes import NodeVisitor


class YAMLDecoder(NodeVisitor):
    def decode(self, s):
        return self.visit(YAMLParser().parse(s))

    def visit_Docs(self, node):
        for doc in node.value:
            yield (yield doc)

    def visit_Doc(self, node):
        for item in node.value:
            yield (yield item)

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

    visit_Null = visit_Scalar
    visit_Str = visit_Scalar
    visit_Int = visit_Scalar
    visit_Float = visit_Scalar
    visit_Bool = visit_Scalar

    def visit_Binary(self, node):
        return node.value
