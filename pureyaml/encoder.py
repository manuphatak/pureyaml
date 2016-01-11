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
        lines = ''.join(line for line in self.iterencode(obj))
        return lines

    def iterencode(self, obj):
        nodes = node_encoder(obj)
        lines = self.visit(nodes)
        lines.append('')
        return '\n'.join(lines)

    def visit_Sequence(self, node):
        lines = []
        template = '{symbol:{width}}{value}'
        for item in node:
            item = iter(self.visit(item))

            kw = {'symbol': '-', 'width': 2, 'value': next(item)}
            lines.append(template.format(**kw))

            kw['symbol'] = ' '
            for line in item:
                kw['value'] = line
                lines.append(template.format(**kw))

        return lines

    def visit_Map(self, node):
        lines = []
        key_value_template = '{key}: {value}'
        key_template = '{key}:'
        value_template = '{indent:{width}}{value}'

        for key, value in node.value:
            if len(key) == len(value) == 1:
                kw = dict(key=self.visit(key)[0], value=self.visit(value)[0])
                lines.append(key_value_template.format(**kw))
            elif len(key) == 1:

                lines.append(key_template.format(key=self.visit(key)[0]))
                for line in self.visit(value):
                    lines.append(value_template.format(indent=' ', width=2, value=line))

        return lines

    def visit_Str(self, node):
        return [str(node.value)]

    def visit_Int(self, node):
        return [str(node.value)]
