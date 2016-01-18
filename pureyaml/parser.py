# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

import logging
from pprint import pformat

from ply.lex import lex
from ply.yacc import yacc

from .exceptions import YAMLSyntaxError, YAMLUnknownSyntaxError
from .grammar.productions import YAMLProductions
from .grammar.tokens import YAMLTokens

logger = logging.getLogger(__name__)


# lex_logger = logging.getLogger('ply.lex')
# yacc_logger = logging.getLogger('ply.yacc')


class YAMLLexer(YAMLTokens):
    @classmethod
    def build(cls, **kwargs):
        self = cls()
        kwargs.setdefault('module', self)
        # kwargs.setdefault('debuglog', lex_logger)
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
        kwargs.setdefault('tabmodule', 'pureyaml.grammar._parsetab')
        kwargs.setdefault('debugfile', '_parser.out')

        self.debug = kwargs.get('debug')
        self.parser = yacc(**kwargs)

    def parse(self, data, **kwargs):
        kwargs.setdefault('lexer', YAMLLexer.build())
        kwargs.setdefault('debug', False)
        return self.parser.parse(data, **kwargs)

    def parsedebug(self, data, **kwargs):
        # TODO use logger
        print(self.tokenize(data))
        kwargs.setdefault('lexer', YAMLLexer.build(debug=True))
        kwargs.setdefault('debug', True)

        return self.parser.parse(data, **kwargs)

    def tokenize(self, data):
        tokens = YAMLLexer.tokenize(data)
        return pformat(list(tokens))

    def p_error(self, p):
        # Guard, empty p
        if p is None:
            raise YAMLUnknownSyntaxError('Unknown origin %r' % p)

        raise YAMLSyntaxError(p)
