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
        try:
            return self.value == other.value and type(self) == type(other)
        except AttributeError:
            return False

    def __repr__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.value)


class Collection(Node):
    def __init__(self, *args):
        self.value = args

    def __add__(self, other):
        Docs = self.__class__

        if isinstance(other, Docs):
            value = self.value + other.value
        else:
            value = self.value + (other,)
        return Docs(*value)


class Docs(Collection):
    pass


class Doc(Node):
    pass


class Sequence(Collection):
    pass


class Map(Collection):
    def __init__(self, *args):
        for arg in args:
            assert len(arg) == 2
        super(Map, self).__init__(*args)


class Scalar(Node):
    type = NotImplemented

    def __init__(self, value):
        self.value = self.type(value)


class Str(Scalar):
    type = str


class Int(Scalar):
    type = int


class Float(Scalar):
    type = float


class Bool(Scalar):
    type = bool
    TRUE_VALUES = [True, 'Yes', 1]
    FALSE_VALUES = [False, 'No', 0]

    def __init__(self, value):
        assert value in self.TRUE_VALUES or value in self.FALSE_VALUES
        self.value = value

    def __eq__(self, other):
        try:
            self_is_true = self.value in self.TRUE_VALUES
            other_is_true = other.value in self.TRUE_VALUES
            return self_is_true == other_is_true and type(self) == type(other)
        except AttributeError:
            return False
