#!/usr/bin/env python
# coding=utf-8
"""
nodes
"""
from __future__ import absolute_import


class Node(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        Node = self.__class__
        if isinstance(other, Node) or hasattr(other, 'value'):
            return self.value == other.value
        else:
            return self.value == other

    def __repr__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.value)


class Docs(Node):
    def __init__(self, *args):
        self.value = args

    def __add__(self, other):
        Docs = self.__class__

        if isinstance(other, (list, tuple, set)):
            value = self.value + other
        elif isinstance(other, Docs):
            value = self.value + other.value
        else:
            value = self.value + (other,)
        return Docs(*value)


class Doc(Node):
    pass


class Scalar(Node):
    type = NotImplemented

    def __init__(self, value):
        self.value = self.type(value)

    def __eq__(self, other):
        if isinstance(other, Scalar) or hasattr(other, 'value'):
            return self.value == self.type(other.value)
        else:
            return self.value == self.type(other)


class String(Scalar):
    type = str


class Int(Scalar):
    type = int


class Sequence(Node):
    def __init__(self):
        self.value = []

    def append(self, value):
        self.value.append(value)


class SequenceItem(Node):
    pass
