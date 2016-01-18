#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from textwrap import dedent


class YAMLException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return str(self.message)


class YAMLUnknownSyntaxError(SyntaxError, YAMLException):
    pass


class YAMLSyntaxError(SyntaxError, YAMLException):
    def __init__(self, p, value=None):
        if value is None:
            value = p.value

        self.value = repr(value)[1:-1]
        self.token = p
        # get cursor position with expanded raw string
        self.offset = len(repr(p.lexer.lexdata[:p.lexpos])[1:-1])
        self.input = repr(p.lexer.lexdata)[1:-1]

    def msg_lines(self):
        yield 'unexpected: %r\n' % self.token

        show_chars = 30
        preview_start = max(0, self.offset - show_chars)
        preview_end = min(len(self.input), len(self.input) + show_chars + 1)

        yield self.input[preview_start:preview_end]

        error_length = max(1, len(self.value))
        pointer = '^' * error_length
        width = len(self.input[preview_start:self.offset - 1] + self.value)
        yield pointer.rjust(width)

    def __str__(self):
        return '\n'.join(self.msg_lines())


class YAMLStrictTypeError(TypeError, YAMLException):
    def __init__(self, token, types, func):
        func_lineno = getattr(func, 'co_firstlineno', func.__code__.co_firstlineno)
        self.module = func.__module__
        self.function = func.__name__
        self.lineno = func_lineno
        self.token_type = type(token).__name__
        self.expected_types = ', '.join(type_.__name__ for type_ in types)
        self.token = token

    def __str__(self):
        return dedent("""
            expected:            {self.expected_types}
            unexpected  type:    {self.token_type}
                |      value:    {self.token!r}
            line:                {self.lineno}
            module:              {self.module}
            function:            {self.function}
        """).format(self=self)


class YAMLCastTypeError(TypeError, YAMLException):
    def __init__(self, message=None, cast=None):
        self.message = message or 'Unexpected cast type: {cast}.  Type not defined'.format(cast=cast)
