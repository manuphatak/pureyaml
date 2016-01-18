#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

# noinspection PyCompatibility
import re

from future.utils import text_type, binary_type, iteritems
from math import isinf, isnan
from .nodes import *  # noqa
from .utils import ContextStack


def node_encoder(obj):  # noqa
    if isinstance(obj, dict):
        items = []
        for key, value in iteritems(obj):
            items.append((node_encoder(key), node_encoder(value)))
        return Map(*items)
    elif isinstance(obj, list):
        items = []
        for item in obj:
            items.append(node_encoder(item))
        return Sequence(*items)
    elif isinstance(obj, binary_type):
        try:
            obj = text_type(obj, 'ascii')
            return Str(obj)
        except UnicodeDecodeError:
            return Binary.from_decoded(obj)
    elif isinstance(obj, text_type):
        try:
            obj.encode('ascii')
            return Str(obj)
        except UnicodeEncodeError:
            obj = binary_type(obj, encoding='utf-8')
            return Binary.from_decoded(obj)
    elif isinstance(obj, bool):
        return Bool(obj)
    elif isinstance(obj, int):
        return Int(obj)
    elif isinstance(obj, type(None)):
        return Null(obj)
    elif isinstance(obj, float):
        return Float(obj)
    else:
        raise RuntimeError('Type %s not supported' % type(obj))


class _ContextStack(ContextStack):
    def __call__(self, text):
        return text.format(**self.attrs)


class SYMBOL:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


INDENT = SYMBOL('INDENT')
DEDENT = SYMBOL('DEDENT')


# noinspection PyMethodMayBeStatic
class YAMLEncoder(NodeVisitor):
    indent_size = 2
    stack = []

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

                indent = ''.ljust(indent_depth * self.indent_size)
                current_item = current_item.replace('\n', '\n{0}'.format(indent))

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
            stack.append('-'.ljust(self.indent_size))
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

    def visit_Map(self, node):
        stack = []
        for k, v in iteritems(node):
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
