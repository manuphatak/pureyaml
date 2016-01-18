#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

import re
from functools import wraps

from ..exceptions import YAMLStrictTypeError


def strict(*types):
    def decorate(func):
        @wraps(func)
        def wrapper(self, p):
            func(self, p)
            if not isinstance(p[0], types):
                raise YAMLStrictTypeError(p[0], types, func)

        wrapper.co_firstlineno = func.__code__.co_firstlineno
        return wrapper

    return decorate


def find_column(t):
    pos = t.lexer.lexpos
    data = t.lexer.lexdata
    last_cr = data.rfind('\n', 0, pos)
    if last_cr < 0:
        last_cr = -1
    column = pos - last_cr
    return column


def rollback_lexpos(t):
    t.lexer.lexpos -= len(t.value)


class fold(object):
    re_folded_repl = re.compile(r"""
          (?P<PARAGRAPH>\n\n)
        | (?P<SPACE>\n)
    """, re.X)

    @classmethod
    def folded_repl(cls, match):
        if match.group('PARAGRAPH') is not None:
            return '\n'
        elif match.group('SPACE') is not None:
            return ' '
        else:
            return match

    def __new__(cls, text):
        return cls.re_folded_repl.sub(cls.folded_repl, text)
