# coding=utf-8
"""Build yacc parser from lex tokens."""
from __future__ import absolute_import

import logging
from os import environ

from .exceptions import YAMLSyntaxError, YAMLUnknownSyntaxError
from .grammar.productions import YAMLProductions
from .grammar.tokens import YAMLTokens
from .ply.lex import lex
from .ply.yacc import yacc

OPTIMIZE = environ.get('PUREYAML_OPTIMIZE', 'true').lower() == 'true'

logger = logging.getLogger(__name__)

lex_logger = logging.getLogger('pureyaml.ply.lex')
yacc_logger = logging.getLogger('pureyaml.ply.yacc')


# noinspection PyMethodMayBeStatic
class YAMLLexer(YAMLTokens):
    @classmethod
    def build(cls, **kwargs):
        self = cls()
        kwargs.setdefault('module', self)
        kwargs.setdefault('debuglog', lex_logger)
        kwargs.setdefault('errorlog', lex_logger)
        if OPTIMIZE or kwargs.get('optimize', False):
            kwargs.setdefault('lextab', 'pureyaml.grammar._lextab')
            kwargs.setdefault('optimize', True)
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


# noinspection PyMethodMayBeStatic
class YAMLParser(YAMLProductions):
    # noinspection PyMissingConstructor
    def __init__(self, **kwargs):
        kwargs.setdefault('debug', False)
        self.debug = kwargs.get('debug')
        self.optimize = OPTIMIZE or kwargs.get('optimize')

        kwargs.setdefault('module', self)
        kwargs.setdefault('tabmodule', 'pureyaml.grammar._parsetab')
        kwargs.setdefault('debugfile', '_parser.out')
        kwargs.setdefault('debuglog', yacc_logger)
        kwargs.setdefault('errorlog', yacc_logger)
        self.parser = yacc(**kwargs)

    def parse(self, data, **kwargs):
        kwargs.setdefault('debug', False)
        kwargs.setdefault('lexer', YAMLLexer.build(optimize=self.optimize))
        return self.parser.parse(data, **kwargs)

    def parsedebug(self, data, **kwargs):
        logger.info('\n'.join(repr(token) for token in self.tokenize(data)))
        kwargs.setdefault('lexer', YAMLLexer.build(debug=True, optimize=False))
        kwargs.setdefault('debug', True)

        return self.parser.parse(data, **kwargs)

    def tokenize(self, data):
        tokens = YAMLLexer.tokenize(data)
        return list(tokens)

    def p_error(self, p):
        # Guard, empty p
        if p is None:
            raise YAMLUnknownSyntaxError('Unknown origin %r' % p)

        raise YAMLSyntaxError(p)
