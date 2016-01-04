# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

from pprint import pformat

from ply.lex import lex
from ply.yacc import yacc

from .grammar import YAMLTokens, YAMLProductions


class YAMLLexer(YAMLTokens):
    @classmethod
    def build(cls, **kwargs):
        self = cls()
        kwargs.setdefault('module', self)
        return lex(**kwargs)

    @classmethod
    def tokenize(cls, data):
        lexer = cls.build()
        lexer.input(data)
        while True:
            token = lexer.token()
            if not token:
                break
            yield token

    def t_ANY_error(self, t):
        raise YAMLSyntaxError(t, t.value[0])


class YAMLParser(YAMLProductions):
    def __init__(self, **kwargs):
        kwargs.setdefault('module', self)
        kwargs.setdefault('tabmodule', '_parsetab')
        kwargs.setdefault('debugfile', '_parser.out')
        self.debug = kwargs.get('debug')
        self.parser = yacc(**kwargs)

    def parse(self, data, **kwargs):
        kwargs.setdefault('lexer', YAMLLexer.build())
        return self.parser.parse(data, **kwargs)

    def parsedebug(self, data, **kwargs):
        print('')
        print(self.tokenize(data))
        kwargs.setdefault('lexer', YAMLLexer.build(debug=True))
        kwargs.setdefault('debug', True)

        return self.parser.parse(data, **kwargs)

    def tokenize(self, data):
        tokens = YAMLLexer.tokenize(data)
        return pformat(list(tokens))

    def p_error(self, p):
        # guard, empty p
        if p is None:
            raise SyntaxError('Unknown origin %s' % p)

        raise YAMLSyntaxError(p)


class YAMLSyntaxError(SyntaxError):
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
