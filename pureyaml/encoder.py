#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

from .nodes import *  # noqa
from .utils import ContextStack


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


class _ContextStack(ContextStack):
    def __call__(self, text):
        return text.format(**self.attrs)


class YAMLEncoder(NodeVisitor):
    indent_size = 2

    @property
    def SEQUENCE_START(self):
        return '-'.ljust(self.indent_size)

    @property
    def INDENT(self):
        return ' ' * self.indent_size

    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        global _
        _ = _ContextStack(self)

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

    def visit_Sequence(self, node):
        lines = []
        for item in node:
            iter_item = iter(self.visit(item))

            _.value = next(iter_item)
            lines.append(_('{self.SEQUENCE_START}{value}'))

            for line in iter_item:
                _.value = line
                lines.append(_('{self.INDENT}{value}'))

        return lines

    def visit_Map(self, node):
        lines = []

        for _key, _value in node.value:
            if isinstance(_key, Scalar) and isinstance(_value, Scalar):
                _.key = self.visit(_key)[0]
                _.value = self.visit(_value)[0]
                lines.append(_('{key}: {value}'))
            elif isinstance(_key, Scalar):
                _.key = self.visit(_key)[0]

                lines.append(_('{key}:'))

                for line in self.visit(_value):
                    _.value = line
                    lines.append(_('{self.INDENT}{value}'))

        return lines

    def visit_Str(self, node):
        return [str(node.value)]

    def visit_Int(self, node):
        return [str(node.value)]
