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
        raise SyntaxError(show_error(t, t.value[0]))


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

        raise SyntaxError(show_error(p, p.value))


class YAMLSyntaxError(SyntaxError):
    pass


def show_error(p, value):
    # setup
    show_chars = 30
    preview_start = max(0, p.lexpos - show_chars)
    preview_end = min(len(p.lexer.lexdata), p.lexpos + show_chars + 1)
    error_length = max(1, len(repr(value)[1:-1]))
    error_end = p.lexpos + error_length
    # line 3
    pre_error_text = p.lexer.lexdata[preview_start:p.lexpos]
    cur_error_text = p.lexer.lexdata[p.lexpos:error_end]
    suf_error_text = p.lexer.lexdata[error_end + 1:preview_end]

    # line 4
    width = len(repr(pre_error_text + cur_error_text)[1:-1])
    error_lines = [  # :off
        '\n',
        'Unexpected value: %r:%r' % (p.type, value),
        repr(pre_error_text + cur_error_text + suf_error_text)[1:-1],
        ('^' * error_length).rjust(width, ' '),
    ]  # :on
    return '\n'.join(error_lines)
