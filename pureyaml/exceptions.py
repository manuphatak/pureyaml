#!/usr/bin/env python
# coding=utf-8

class YAMLException(Exception):
    pass


class YAMLUnknownSyntaxError(SyntaxError, YAMLException):
    pass


class YAMLSyntaxError(SyntaxError, YAMLException):
    def __init__(self, p, value=None):
        if value is None:
            value = p.value

        self.value = repr(value)[1:-1]
        self.token = p
        self.offset = p.lexpos
        self.input = repr(p.lexer.lexdata)[1:-1]

    def msg_lines(self):
        yield 'unexpected: %r\n' % self.token

        show_chars = 30
        preview_start = max(0, self.offset - show_chars)
        preview_end = min(len(self.input), len(self.input) + show_chars + 1)

        yield self.input[preview_start:preview_end]

        error_length = max(1, len(self.value))
        pointer = '^' * error_length
        width = self.offset + len(self.value)
        yield pointer.rjust(width)

    def __str__(self):
        return '\n'.join(self.msg_lines())


class YAMLStrictTypeError(TypeError, YAMLException):
    def __init__(self, token, types, func):
        func_lineno = getattr(func, 'co_firstlineno', func.__code__.co_firstlineno)
        qualname = '%s.%s:%d' % (func.__module__, func.__name__, func_lineno)
        link = '%s:%i' % (func.__code__.co_filename, func_lineno)
        token_type = type(token).__name__
        expected_types = ', '.join(type_.__name__ for type_ in types)
        msg = ('\nunexpected type: %r'
               '\nexpected:        %r'
               '\n                 %r'
               '\nlocation:        %r'
               '\nlink:            %s'

               ) % (token_type, expected_types, token, qualname, link)
        super(YAMLStrictTypeError, self).__init__(msg)
