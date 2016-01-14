#!/usr/bin/env python
# coding=utf-8
"""
nodes
"""
from __future__ import absolute_import

import re
import types
from base64 import standard_b64decode, standard_b64encode
from functools import partial
from math import isnan

from future.utils import implements_iterator, iteritems, binary_type, text_type

from ._compat import collections_abc as abc
from .exceptions import YAMLCastTypeError


class Node(object):
    def __init__(self, value, **kwargs):
        self.raw_value = value
        self.value = self.init_value(self, value, **kwargs)

    def init_value(self, *values, **kwargs):
        return values[0]

    def __eq__(self, other):
        try:
            return self.value == other.value and type(self) == type(other)
        except AttributeError:
            return False

    def __ne__(self, other):
        return not (self == other)

    def repr_value(self, value):
        return repr(value)

    def __repr__(self):
        cls_name = self.__class__.__name__

        try:
            value = self.repr_value(self.value)
        except AttributeError:
            value = self.repr_value(self.raw_value)

        return '<%s:%s>' % (cls_name, value)


@implements_iterator
class SequenceMixin(abc.Sequence):
    value = NotImplemented

    def __init__(self, *args, **kwargs):
        super(SequenceMixin, self).__init__(*args, **kwargs)
        self._iter = iter(self.value)

    def __getitem__(self, index):
        return self.value[index]

    def __len__(self):
        return len(self.value)

    def __contains__(self, x):
        return x in self.value

    def __next__(self):
        return next(self._iter)

    def __iter__(self):
        return self


class Collection(SequenceMixin, Node):
    def __init__(self, *values, **kwargs):
        self.raw_value = values
        self.value = self.init_value(*values, **kwargs)
        self._iter = iter(self.value)

    def init_value(self, *value, **kwargs):
        return value

    def __add__(self, other):
        _Collection = self.__class__

        if not isinstance(other, _Collection):
            self_cls_name, other_cls_name = self.__class__.__name__, other.__class__.__name__
            raise TypeError('%s + %s :: %s + %s' % (self_cls_name, other_cls_name, self, other))

        value = self.value + other.value
        return _Collection(*value)


class Docs(Collection):
    pass


class Doc(Collection):
    pass


class Sequence(Collection):
    pass


@implements_iterator
class MappingMixin(abc.Mapping):
    value = NotImplemented

    def __init__(self, *args, **kwargs):
        super(MappingMixin, self).__init__(*args, **kwargs)
        self._iter = iter(self.value)

    def __getitem__(self, key):
        for k, v in self.value:
            if k == key:
                return v

        raise KeyError('key %s not found in %r' % (key, self))

    def __len__(self):
        return len(self.value)

    def __next__(self):
        _next = next(self._iter)[0]
        return _next

    def __iter__(self):
        return self


class Map(MappingMixin, Collection):
    def init_value(self, *values, **kwargs):
        for value in values:
            if len(value) == 2:
                continue

            msg = 'Unexpected Value: %s :: %s values must come in pairs'
            cls_name = self.__class__.__name__
            raise ValueError(msg % (value, cls_name))

        return values

    def __eq__(self, other):  # noqa
        if type(self) != type(other):
            return False

        for key, self_value in iteritems(self):
            try:
                other_value = other[key]
            except KeyError:
                return False

            if self_value != other_value:
                return False

        if len(self) != len(other):
            return False

        return True


class Scalar(Node):
    type = NotImplemented

    def __init__(self, value, *args, **kwargs):
        self.raw_value = value
        self.value = self.init_value(value, *args, **kwargs)

    def init_value(self, value, *args, **kwargs):
        return self.type(value)

    def __len__(self):
        return 1


class Null(Scalar):
    type = None

    def init_value(self, *values, **kwargs):
        return None


class Str(Scalar):
    type = str

    def init_value(self, value, *args, **kwargs):
        if value is None:
            return ''
        return super(Str, self).init_value(value, *args, **kwargs)


class Int(Scalar):
    type = int

    def init_value(self, value, base=None, *args, **kwargs):
        if base is not None:
            return self.type(value, base=base)

        return self.type(value)


class Float(Scalar):
    type = float

    def init_value(self, value, *args, **kwargs):
        # Guard, inf and nan
        if isinstance(value, str):
            value_lower = value.lower().replace('.', '')
            if value_lower.endswith('inf'):
                return self.type(value_lower)
            if value_lower.endswith('nan'):
                return self.type(value_lower)

        return self.type(value)

    def __eq__(self, other):
        # Guard, we're not doing math.
        if isnan(self.value) and isnan(other.value):
            return True

        return super(Float, self).__eq__(other)


class Bool(Scalar):
    type = bool
    TRUE_VALUES = ['TRUE', 'YES', '1']
    FALSE_VALUES = ['FALSE', 'NO', '0']

    def init_value(self, value, *args, **kwargs):
        str_value = str(value).upper()
        possible_values = self.TRUE_VALUES + self.FALSE_VALUES
        if str_value not in possible_values:
            cls_name = self.__class__.__name__
            msg = 'Unknown %s value: %r not in %s'
            raise ValueError(msg % (cls_name, value, possible_values))
        return str_value in self.TRUE_VALUES


class Binary(Scalar):
    type = 'binary'

    def init_value(self, value, *args, **kwargs):
        if isinstance(value, text_type):
            value = binary_type(value, 'ascii')
        return standard_b64decode(value)

    @classmethod
    def from_decoded(cls, data):
        self = cls.__new__(cls)
        self.raw_value = data
        self.raw_value = standard_b64encode(data).decode('ascii')
        self.value = standard_b64decode(self.raw_value)
        return self


class ScalarDispatch(object):
    map = {  # :off
        'null': Null,
        'bool': Bool,
        'int': Int,
        'int10': partial(Int, base=10),
        'int8': partial(Int, base=8),
        'int16': partial(Int, base=16),
        'float': Float,
        'infinity': Float,
        'nan': Float,
        'str': Str,
        'binary': Binary,
    }  # :on

    re_dispatch = re.compile(r"""
        ^ (?P<null> (?i) null $| ~ $)
        | (?P<bool> (?i) true $| false $| yes $| no $)
        | (?P<int10> [-+]? [0-9]+ $)
        | (?P<int8> 0o [0-7]+ $)
        | (?P<int16> 0x [0-9a-fA-F]+ $)
        | (?P<float>[-+]? (?:
            (?: [0-9]* \. [0-9]+ |  [0-9]+ \. [0-9]* )
                (?: [eE] [-+]? [0-9]+ )? $|
            [0-9]* \.? [0-9]* [eE] [-+]? [0-9]+ ) $
          )
        | (?P<infinity> [-+]? (?: \.inf | \.Inf | \.INF) $)
        | (?P<nan> [-+]? (?: \.nan | \.NaN | \.NAN) $)
        | (?P<str> .+ $)
    """, re.X)

    def __new__(cls, value, cast=None):  # noqa
        # Guard, explicit casting
        if cast is not None:
            try:
                return cls.map[cast](value)
            except KeyError:
                raise YAMLCastTypeError(cast=cast)

        # Guard, already casted
        type_name = type(value).__name__
        if not isinstance(value, str) and type_name in cls.map:
            return cls.map[type_name](value)

        # Guard, empty value
        value = value.strip()
        if value == '':
            return Null(value)

        match = cls.re_dispatch.match(value)
        return cls.map[match.lastgroup](value)


class NodeVisitor(object):
    def __init__(self, *args, **kwargs):
        pass

    def visit(self, node):
        stack = [node]
        last_result = None
        while stack:
            try:
                last = stack[-1]
                if isinstance(last, types.GeneratorType):
                    sent = last.send(last_result)
                    stack.append(sent)
                    last_result = None
                elif isinstance(last, Node):
                    stack.append(self._visit(stack.pop()))
                else:
                    last_result = stack.pop()
            except StopIteration:
                stack.pop()
        return last_result

    def _visit(self, node):
        method_name = 'visit_%s' % type(node).__name__
        method = getattr(self, method_name, None)

        if method is None:
            method = self.generic_visit
        return method(node)

    def generic_visit(self, node):
        raise RuntimeError('No visit_%s method' % type(node).__name__)


__all__ = ['Node', 'Collection', 'Docs', 'Doc', 'Sequence', 'Map', 'Scalar', 'Null', 'Str', 'Int', 'Float', 'Bool',
           'Binary', 'ScalarDispatch', 'NodeVisitor', ]
