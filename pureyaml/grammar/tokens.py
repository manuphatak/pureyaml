# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

from textwrap import dedent

from .utils import find_column, rollback_lexpos
from ..exceptions import YAMLUnknownSyntaxError


class TokenList(object):
    tokens = [  # :off
        'DOC_START',
        'DOC_END',
        'B_SEQUENCE_COMPACT_START',
        'B_SEQUENCE_START',
        'B_MAP_COMPACT_KEY',
        'B_MAP_COMPACT_VALUE',
        'B_MAP_KEY',
        'B_MAP_VALUE',
        'B_LITERAL_START',
        'B_LITERAL_END',
        'B_FOLD_START',
        'B_FOLD_END',
        'DOUBLEQUOTE_START',
        'DOUBLEQUOTE_END',
        'SINGLEQUOTE_START',
        'SINGLEQUOTE_END',
        'CAST_TYPE',
        'SCALAR',
        'INDENT',
        'DEDENT',
        'F_SEQUENCE_START',
        'F_SEQUENCE_END',
        'F_MAP_START',
        'F_MAP_END',
        'F_MAP_KEY',
        'F_SEP',

    ]  # :on


# noinspection PyMethodMayBeStatic,PyIncorrectDocstring,PySingleQuotedDocstring,PyPep8Naming
class YAMLTokens(TokenList):
    def __init__(self):
        self.indent_stack = [1]

    def get_indent_status(self, t):
        column = find_column(t)
        curr_depth, next_depth = self.indent_stack[-1], column

        if next_depth > curr_depth:
            status = 'INDENT'
        elif next_depth < curr_depth:
            status = 'DEDENT'
        else:
            status = 'NODENT'

        return status, curr_depth, next_depth

    # LEXER
    # ===================================================================
    states = (  # :off
        ('tag', 'inclusive'),
        ('doublequote', 'exclusive'),
        ('comment', 'exclusive'),
        ('singlequote', 'exclusive'),
        ('literal', 'exclusive'),
        ('fold', 'exclusive'),
        ('flowsequence', 'exclusive'),
        ('flowmap', 'exclusive'),
    )  # :on

    literals = '"'

    # state: multiple
    # -------------------------------------------------------------------

    def t_ignore_INDENT(self, t):
        r'\n\s*'

        indent_status, curr_depth, next_depth = self.get_indent_status(t)

        if indent_status == 'NODENT':
            return

        if indent_status == 'INDENT':
            # note: also set by
            #   * t_B_SEQUENCE_COMPACT_START
            #   * t_B_MAP_COMPACT_KEY
            #   * t_B_MAP_COMPACT_VALUE
            self.indent_stack.append(next_depth)

        if indent_status == 'DEDENT':
            indent_delta = curr_depth - next_depth
            step = self.indent_stack.pop() - self.indent_stack[-1]

            # If dedent is larger then last indent
            if indent_delta > step:
                # Go back and reevaluate this token.
                rollback_lexpos(t)

        t.type = indent_status
        return t

    # state: tag
    # -------------------------------------------------------------------
    def t_begin_tag(self, t):
        r'(?<!\\)!'
        t.lexer.push_state('tag')

    def t_tag_end(self, t):
        r'\ '
        t.lexer.pop_state()

    def t_tag_CAST_TYPE(self, t):
        r'(?<=\!)[a-z]+'
        return t

    # state: doublequote
    # -------------------------------------------------------------------
    t_doublequote_SCALAR = r'(?:\\"|[^"])+'

    def t_begin_doublequote(self, t):
        r'(?<!\\)"'

        t.lexer.push_state('doublequote')
        t.type = 'DOUBLEQUOTE_START'
        return t

    def t_doublequote_end(self, t):
        r'(?<!\\)"'
        t.lexer.pop_state()
        t.type = 'DOUBLEQUOTE_END'
        return t

    # state: comment
    # -------------------------------------------------------------------
    t_comment_ignore_COMMENT = r'[^\n]+'

    def t_begin_comment(self, t):
        r'\s*\#\ ?'
        t.lexer.push_state('comment')
        # t.lexer.begin('comment')

    def t_comment_end(self, t):
        r'(?=\n)'
        # t.lexer.begin('INITIAL')
        t.lexer.pop_state()

    # state: singlequote
    # -------------------------------------------------------------------
    t_singlequote_SCALAR = r"(?:\\'|[^']|'')+"

    def t_begin_singlequote(self, t):
        r"(?<!\\)'"
        t.lexer.push_state('singlequote')
        # t.lexer.begin('singlequote')
        t.type = 'CAST_TYPE'
        t.type = 'SINGLEQUOTE_START'
        return t

    def t_singlequote_end(self, t):
        r"(?<!\\)'"
        t.lexer.pop_state()
        t.type = 'SINGLEQUOTE_END'
        return t

    # state: literal
    # -------------------------------------------------------------------
    t_literal_SCALAR = r'.+'

    def t_begin_literal(self, t):
        r'\ *(?<!\\)\|\ ?\n'
        t.lexer.push_state('literal')
        t.type = 'B_LITERAL_START'
        return t

    def t_literal_end(self, t):
        r'\n+\ *'
        column = find_column(t)
        indent = self.indent_stack[-1]
        if column < indent:
            rollback_lexpos(t)
        if column <= indent:
            t.lexer.pop_state()
            t.type = 'B_LITERAL_END'
        if column > indent:
            t.type = 'SCALAR'
        return t

    # state: fold
    # -------------------------------------------------------------------
    t_fold_SCALAR = r'.+'

    def t_begin_fold(self, t):
        r'\ *(?<!\\)\>\ ?\n'
        t.lexer.push_state('fold')
        t.type = 'B_FOLD_START'
        return t

    def t_fold_end(self, t):
        r'\n+\ *'
        column = find_column(t)
        indent = self.indent_stack[-1]
        if column < indent:
            rollback_lexpos(t)
        if column <= indent:
            t.lexer.pop_state()
            t.type = 'B_FOLD_END'
        if column > indent:
            t.type = 'SCALAR'
        return t

    # state: flowsequence
    # -------------------------------------------------------------------
    def t_flowsequence_flowmap_F_SEP(self, t):
        r','
        return t

    # state: flowsequence
    # -------------------------------------------------------------------
    t_flowsequence_SCALAR = r'[^\[\],]+'

    def t_begin_flowsequence(self, t):
        r'\['
        t.lexer.push_state('flowsequence')
        t.type = 'F_SEQUENCE_START'
        return t

    def t_flowsequence_end(self, t):
        r'\]'
        t.lexer.pop_state()
        t.type = 'F_SEQUENCE_END'
        return t

    # state: flowmap
    # -------------------------------------------------------------------
    t_flowmap_SCALAR = r'[^\{\}\:,]+'

    def t_flowmap_F_MAP_KEY(self, t):
        r'\:\ ?'
        return t

    def t_begin_flowmap(self, t):
        r'\{'
        t.lexer.push_state('flowmap')
        t.type = 'F_MAP_START'
        return t

    def t_flowmap_end(self, t):
        r'\}'
        t.lexer.pop_state()
        t.type = 'F_MAP_END'

        return t

    # state: INITIAL
    # -------------------------------------------------------------------
    t_ignore_EOL = r'\s*\n'

    def t_DOC_START(self, t):
        r'\-\-\-'
        return t

    def t_DOC_END(self, t):
        r'\.\.\.'
        return t

    def t_B_SEQUENCE_COMPACT_START(self, t):
        r"""
          \-\ + (?=  -\   )
          #          ^ ^ sequence indicator
        | \-\ + (?=  [\{\[]\   |  [^:\n]*:\s   )
          #            ^ ^          ^^^ map indicator
          #            ^ ^ flow indicator
        """
        indent_status, curr_depth, next_depth = self.get_indent_status(t)

        if indent_status == 'INDENT':
            self.indent_stack.append(next_depth)
            return t

        msg = dedent("""
            expected 'INDENT', got  {indent_status!r}
            current_depth:          {curr_depth}
            next_depth:             {next_depth}
            token:                  {t}
        """).format(**vars())

        raise YAMLUnknownSyntaxError(msg)

    def t_B_SEQUENCE_START(self, t):
        r'-\ +|-(?=\n)'
        return t

    def t_B_MAP_COMPACT_KEY(self, t):
        r"""
          \?\ + (?=  -\   )
          #          ^ ^ sequence indicator
        | \?\ + (?=  [\{\[]\   |  [^:\n]*:\s   )
          #            ^ ^          ^^^ map indicator
          #            ^ ^ flow indicator
        """
        indent_status, curr_depth, next_depth = self.get_indent_status(t)

        if indent_status == 'INDENT':
            self.indent_stack.append(next_depth)
            return t

        msg = dedent("""
            expected 'INDENT', got  {indent_status!r}
            current_depth:          {curr_depth}
            next_depth:             {next_depth}
            token:                  {t}
        """).format(**vars())

        raise YAMLUnknownSyntaxError(msg)

    def t_B_MAP_COMPACT_VALUE(self, t):
        r"""
          \:\ + (?=  -\   )
          #          ^ ^ sequence indicator
        | \:\ + (?=  [\{\[]\   |  [^:\n]*:\s   )
          #            ^ ^          ^^^ map indicator
          #            ^ ^ flow indicator
        """
        indent_status, curr_depth, next_depth = self.get_indent_status(t)

        if indent_status == 'INDENT':
            self.indent_stack.append(next_depth)
            return t

        msg = dedent("""
            expected 'INDENT', got  {indent_status!r}
            current_depth:          {curr_depth}
            next_depth:             {next_depth}
            token:                  {t}
        """).format(**vars())

        raise YAMLUnknownSyntaxError(msg)

    def t_B_MAP_KEY(self, t):
        r'\?\ +|\?(?=\n)'
        return t

    def t_B_MAP_VALUE(self, t):
        r':\ +|:(?=\n)'
        return t

    def t_SCALAR(self, t):
        r'(?:\\.|[^\n\#\:\-\|\>]|[\:\-\|\>]\S)+'
        return t
