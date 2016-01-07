#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

import re


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
