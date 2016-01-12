#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

from contextlib import contextmanager

from .nodes import *  # noqa
from .utils import AttributeContextStack


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


_ = AttributeContextStack()


def expand(text):
    return text.format_map(_)


class YAMLEncoder(NodeVisitor):
    indent_size = 2
    indent_depth = 0
    EMPTY = ''
    MINUS = '-'
    t_INDENT = '{self.EMPTY:<{width}}'

    @property
    def s_INDENT(self):
        _.width = self.indent_size * self.indent_depth
        return expand(self.t_INDENT)

    @contextmanager
    def indent(self):
        self.indent_depth += 1
        yield
        self.indent_depth -= 1

    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        _.self = self

    def _visit(self, node):
        with _.context():
            return super(YAMLEncoder, self)._visit(node)

    def encode(self, obj):
        lines = ''.join(line for line in self.iterencode(obj))
        return lines

    def iterencode(self, obj):
        nodes = node_encoder(obj)
        lines = self.visit(nodes)
        lines.append('')
        return '\n'.join(lines)

    t_SEQUENCE_INDICATOR = '{self.MINUS:<{self.indent_size}}'
    t_SEQUENCE = '{prefix}{value}'

    @property
    def s_SEQUENCE_INDICATOR(self):
        return expand(self.t_SEQUENCE_INDICATOR)

    def visit_Sequence(self, node):
        lines = []

        for item in node:
            iter_item = iter(self.visit(item))

            _.prefix = self.s_SEQUENCE_INDICATOR
            _.value = next(iter_item)
            lines.append(expand(self.t_SEQUENCE))

            _.prefix = ''
            for line in iter_item:
                _.value = line
                lines.append(expand('{value}'))

        return lines

    t_MAP_INLINE = '{self.s_INDENT}{key}: {value}'
    t_MAP_KEY = '{self.s_INDENT}{key}:'
    t_MAP_VALUE = '{self.s_INDENT}{value}'

    def visit_Map(self, node):
        lines = []

        for _key, _value in node.value:
            if isinstance(_key, Scalar) and isinstance(_value, Scalar):
                _.key = self.visit(_key)[0]
                _.value = self.visit(_value)[0]
                lines.append(expand(self.t_MAP_INLINE))
            elif isinstance(_key, Scalar):
                _.key = self.visit(_key)[0]

                lines.append(expand(self.t_MAP_KEY))

                for line in self.visit(_value):
                    _.value = line
                    with self.indent():
                        lines.append(expand(self.t_MAP_VALUE))

        return lines

    def visit_Str(self, node):
        return [str(node.value)]

    def visit_Int(self, node):
        return [str(node.value)]
