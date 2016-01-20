#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

import re
from math import isinf, isnan

from future.utils import text_type, binary_type, iteritems

from ._compat import singledispatch
from .nodes import *  # noqa


@singledispatch
def node_encoder(obj):  # noqa
    """Convert python object to node tree."""
    raise RuntimeError('Type %s not supported' % type(obj))


@node_encoder.register(dict)
def _(obj):
    items = []
    for key, value in iteritems(obj):
        items.append((node_encoder(key), node_encoder(value)))
    return Map(*items)


@node_encoder.register(list)  # noqa
def _(obj):
    items = []
    for item in obj:
        items.append(node_encoder(item))
    return Sequence(*items)


@node_encoder.register(binary_type)  # noqa
def _(obj):
    try:
        obj = text_type(obj, 'ascii')
        return Str(obj)
    except UnicodeDecodeError:
        return Binary.from_decoded(obj)


@node_encoder.register(text_type)  # noqa
def _(obj):
    try:
        obj.encode('ascii')
        return Str(obj)
    except UnicodeEncodeError:
        obj = binary_type(obj, encoding='utf-8')
        return Binary.from_decoded(obj)


@node_encoder.register(bool)  # noqa
def _(obj):
    return Bool(obj)


@node_encoder.register(int)  # noqa
def _(obj):
    return Int(obj)


@node_encoder.register(float)  # noqa
def _(obj):
    return Float(obj)


@node_encoder.register(type(None))  # noqa
def _(obj):
    return Null(obj)


class SYMBOL:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


INDENT = SYMBOL('INDENT')
DEDENT = SYMBOL('DEDENT')


# noinspection PyMethodMayBeStatic
class YAMLEncoder(NodeVisitor):
    """Convert node tree into string."""
    stack = []

    def __init__(self, indent=None, sort_keys=None, **kw):
        super(YAMLEncoder, self).__init__(**kw)
        self.indent = indent or 2
        self.sort_keys = sort_keys or False

    def encode(self, obj):
        lines = ''.join(line for line in self.iterencode(obj))
        return lines

    def iterencode(self, obj):
        stack = []
        for chunk in self._encode(obj):
            stack.append(chunk)
            if not chunk.endswith('\n'):
                continue

            yield ''.join(stack)
            stack = []

        yield ''.join(stack)

    def _encode(self, obj):  # noqa

        indent_depth = 0
        nodes = node_encoder(obj)
        items = self.visit(nodes)
        items = iter(items)
        next_item = next(items)
        while True:
            try:
                current_item, next_item = next_item, next(items)

                if next_item == '\n':
                    current_item = current_item.rstrip(' ')

                if next_item is INDENT:
                    indent_depth += 1
                    next_item = current_item
                    continue

                if next_item is DEDENT:
                    indent_depth -= 1
                    next_item = current_item
                    continue

                indent_spaces = ''.ljust(indent_depth * self.indent)
                current_item = current_item.replace('\n', '\n{0}'.format(indent_spaces))

                yield current_item

            except StopIteration:
                yield next_item
                if next_item != '\n':
                    yield '\n'
                if not isinstance(nodes, (Collection, Str)):
                    yield '...\n'
                break

    def visit_Sequence(self, node):
        stack = []
        for child in node:
            stack.append('-'.ljust(self.indent))
            item = (yield child)
            if not isinstance(item, list):
                stack.append(item)
                stack.append('\n')
            else:
                iter_items = iter(item)
                while True:
                    next_item = next(iter_items)
                    stack.append(next_item)
                    if next_item == '\n':
                        break
                stack.append(INDENT)
                stack.extend([next_item for next_item in iter_items])
                stack.append(DEDENT)

        yield stack

    def iter_map_items(self, node):
        if not isinstance(node, Map):
            raise TypeError('Expecting %r, got %r' % (Map, type(node)))
        if self.sort_keys is False:
            for k, v in iteritems(node):
                yield k, v
        else:
            for k in iter(sorted(node)):
                yield k, node[k]

    def visit_Map(self, node):
        stack = []
        for k, v in self.iter_map_items(node):
            key, value = (yield k), (yield v)
            is_oneliner = not isinstance(key, list) and not isinstance(value, list)
            is_compact_key = isinstance(v, Scalar) and isinstance(value, list)
            is_complex_key = isinstance(key, list)
            if is_oneliner:
                stack.append((yield key))
                stack.append(': ')
                stack.append((yield value))
                stack.append('\n')
            elif is_compact_key:
                stack.append((yield key))
                stack.append(': ')
                stack.extend(value)
                stack.append('\n')
            elif not is_complex_key:
                stack.append((yield key))
                stack.append(': ')
                stack.append('\n')
                if isinstance(v, Sequence):
                    # special case, Map value -> Sequence has optional indent.
                    stack.extend(value)
                else:
                    stack.append(INDENT)
                    stack.extend(value)
                    stack.append(DEDENT)

        yield stack

    def visit_Scalar(self, node):
        return repr(node.value)

    def visit_Str(self, node):
        value = text_type(node.value)
        if not value:
            return '""'
        use_repr = any([  # :off
            value.lower() in ['yes', 'no', 'true', 'false'],
            value.isnumeric(),
            is_float(value)
        ])  # :on

        method = repr if use_repr else str
        if value.endswith('\n') and '\n' in value[:-1]:
            stack = ['|\n', INDENT]
            stack.extend(method(node.value).splitlines(True))
            stack.append(DEDENT)
            return stack

        if value.endswith('\n'):
            return ['>\n', INDENT, method(node.value), DEDENT]
        return method(node.value)

    def visit_Bool(self, node):
        return self.visit_Scalar(node).lower()

    visit_Int = visit_Scalar

    def visit_Float(self, node):
        if isnan(node.value):
            return '.nan'
        if isinf(node.value):
            return repr(node.value).replace('inf', '.inf')

        return repr(node.value)

    # noinspection PyUnusedLocal
    def visit_Null(self, node):
        return 'null'

    def visit_Binary(self, node):
        stack = ['!!binary |\n', INDENT]
        stack.extend(node.raw_value.splitlines(True))
        stack.append(DEDENT)
        return stack


re_float = re.compile(r'[+-]?(?:\d*\.\d+|\d+\.\d)')


def is_float(string):
    return not not re_float.match(string)
