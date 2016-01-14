#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

# noinspection PyCompatibility
from future.utils import text_type, binary_type, iteritems

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


class YAMLEncoder(NodeVisitor):
    indent_size = 2
    stack = []

    def encode(self, obj):
        lines = ''.join(line for line in self.iterencode(obj))
        return lines

    def iterencode(self, obj):
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

                if next_item == 'INDENT':
                    indent_depth += 1
                    next_item = current_item
                    continue

                if next_item == 'DEDENT':
                    indent_depth -= 1
                    next_item = current_item
                    continue

                if current_item == '\n':
                    yield '\n{indent}'.format(indent=' ' * indent_depth * self.indent_size)
                else:
                    yield current_item

            except StopIteration:
                yield next_item
                break

    def visit_Sequence(self, node):
        stack = []
        for item in node:
            stack.append('-'.ljust(self.indent_size))
            item_value = (yield item)
            if not isinstance(item_value, list):
                stack.append(item_value)
                stack.append('\n')
            else:
                iter_items = iter(item_value)
                while True:
                    next_item = next(iter_items)
                    stack.append(next_item)
                    if next_item == '\n':
                        break
                stack.append('INDENT')
                stack.extend([next_item for next_item in iter_items])
                stack.append('DEDENT')

        yield stack

    def visit_Map(self, node):
        stack = []
        for key, value in iteritems(node):
            key, value = (yield key), (yield value)
            if not isinstance(key, list) and not isinstance(value, list):
                stack.append((yield key))
                stack.append(': ')
                stack.append((yield value))
                stack.append('\n')
            elif not isinstance(key, list):
                stack.append((yield key))
                stack.append(': ')
                stack.append('\n')
                stack.append('INDENT')
                stack.extend(value)
                stack.append('DEDENT')

        yield stack

    def visit_Scalar(self, node):
        return repr(node.value)

    def visit_Str(self, node):
        value = text_type(node.value)
        repr_required = [  # :off
            value.isdecimal(),
            value.lower() in ['yes', 'no', 'true', 'false'],
        ]  # :on

        method = repr if any(repr_required) else str

        return method(node.value)

    visit_Int = visit_Scalar
    visit_Bool = visit_Scalar
    visit_Float = visit_Scalar
