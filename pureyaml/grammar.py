# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

from functools import wraps
from textwrap import dedent

from .exceptions import YAMLStrictTypeError, YAMLUnknownSyntaxError
from .nodes import *  # noqa
from .utils import fold


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


class TokenList(object):
    tokens = [  # :off
        'DOC_START',
        'DOC_END',
        'B_SEQUENCE_COMPACT_START',
        'B_SEQUENCE_START',
        'B_MAP_KEY',
        'B_MAP_VALUE',
        'B_LITERAL_START',
        'B_LITERAL_END',
        'B_FOLD_START',
        'B_FOLD_END',
        'DOUBLEQUOTE_START',
        'DOUBLEQUOTE_END',
        'DOUBLEQUOTE_NL',
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


# noinspection PyMethodMayBeStatic,PyIncorrectDocstring,PySingleQuotedDocstring
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
            # note: also set by t_B_SEQUENCE_COMPACT_START
            self.indent_stack.append(next_depth)

        if indent_status == 'DEDENT':
            indent_delta = curr_depth - self.indent_stack.pop()
            t.lexer.lexpos -= indent_delta

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
            # TODO rollback and dedent
            raise Exception('TODO, dedent')
        elif column == indent:
            t.lexer.pop_state()
            t.type = 'B_LITERAL_END'
            return t
        else:
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
            # TODO rollback and dedent
            raise Exception('TODO, dedent')
        elif column == indent:
            t.lexer.pop_state()
            t.type = 'B_FOLD_END'
            return t
        else:
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
          -\ +(?=-)                     # + sequence indicator
        | -\ +(?![\{\[])                # - flow indicator
            (?=[^:\n]*:\ )              # + map indicator
        """
        indent_status, curr_depth, next_depth = self.get_indent_status(t)

        if indent_status != 'INDENT':
            msg = dedent("""
                expected 'INDENT', got %r
                current_depth:      %s
                next_depth:         %s
                token:              %s
            """)
            raise YAMLUnknownSyntaxError(msg % (  # :off
                indent_status,
                curr_depth,
                next_depth,
                t
            ))  # :on

        self.indent_stack.append(next_depth)
        return t

    def t_B_SEQUENCE_START(self, t):
        r'-\ +|-(?=\n)'
        return t

    def t_B_MAP_KEY(self, t):
        r'\?\ +|\?(?=\n)'
        return t

    def t_B_MAP_VALUE(self, t):
        r':\ +|:(?=\n)'
        return t

    def t_SCALAR(self, t):
        r'(?:\\.|[^\n\#\:\-\|]|[\:\-\|]\S)+'
        return t


# noinspection PyIncorrectDocstring
class YAMLProductions(TokenList):
    # PARSER
    # ===================================================================
    @strict(Docs)
    def p_docs_last(self, p):
        """
        docs    : doc
        """
        p[0] = Docs(p[1])

    @strict(Docs)
    def p_docs_init(self, p):
        """
        docs    : docs doc
        """
        p[0] = p[1] + Docs(p[2])

    @strict(Doc)
    def p_doc_indent(self, p):
        """
        doc : DOC_START doc DOC_END
            | DOC_START doc
            | INDENT doc DEDENT
        """
        p[0] = p[2]

    @strict(Doc)
    def p_doc(self, p):
        """
        doc : collection
            | scalar
        """
        p[0] = Doc(p[1])

    @strict(Sequence, Map)
    def p_collection(self, p):
        """
        collection  : sequence
                    | map
                    | flow_collection
        """
        p[0] = p[1]

    @strict(Map)
    def p_map_last(self, p):
        """
        map : map_item
        """
        p[0] = Map(p[1])

    @strict(Map)
    def p_map_init(self, p):
        """
        map : map map_item
        """
        p[0] = p[1] + Map(p[2])

    @strict(tuple)
    def p_map_item(self, p):
        """
        map_item    : map_item_key map_item_value
        """
        p[0] = p[1], p[2]

    @strict(Scalar)
    def p_map_item_complex_key_scalar(self, p):
        """
        map_item_key    : B_MAP_KEY scalar
        """
        p[0] = p[2]

    @strict(Scalar)
    def p_map_item_key(self, p):
        """
        map_item_key    : scalar
        """
        p[0] = p[1]

    @strict(Map, Sequence)
    def p_map_item_value_collection(self, p):
        """
        map_item_value  :  B_MAP_VALUE INDENT collection DEDENT
        """
        p[0] = p[3]

    @strict(Map, Sequence)
    def p_map_item_value_flow_collection(self, p):
        """
        map_item_value  :  B_MAP_VALUE flow_collection
        """
        p[0] = p[2]

    @strict(Scalar)
    def p_map_item_value_scalar(self, p):
        """
        map_item_value  : B_MAP_VALUE scalar
        """
        p[0] = p[2]

    # @strict(Null)
    # def p_map_item_value_empty(self, p):
    #     """
    #     map_item_value  : B_MAP_VALUE empty
    #     """
    #     p[0] = Null(None)

    @strict(Sequence)
    def p_sequence_last(self, p):
        """
        sequence    : sequence_item
        """
        p[0] = Sequence(p[1])

    @strict(Sequence)
    def p_sequence_init(self, p):
        """
        sequence    : sequence sequence_item
        """
        p[0] = p[1] + Sequence(p[2])

    @strict(Scalar)
    def p_sequence_item_scalar(self, p):
        """
        sequence_item   : B_SEQUENCE_START scalar
        """
        p[0] = p[2]

    # @strict(Null)
    # def p_sequence_item_scalar_empty(self, p):
    #     """
    #     sequence_item   : B_SEQUENCE_START empty
    #     """
    #     p[0] = Null(None)

    @strict(Map, Sequence)
    def p_sequence_item_collection(self, p):
        """
        sequence_item   : B_SEQUENCE_START INDENT collection DEDENT
        """
        p[0] = p[3]

    @strict(Map, Sequence)
    def p_sequence_item_compact_collection(self, p):
        """
        sequence_item   : B_SEQUENCE_COMPACT_START collection DEDENT
        """
        p[0] = p[2]

    @strict(Map, Sequence)
    def p_sequence_item_flow_collection(self, p):
        """
        sequence_item   : B_SEQUENCE_START flow_collection
        """
        p[0] = p[2]

    @strict(Str)
    def p_scalar_doublequote(self, p):
        """
        scalar  : DOUBLEQUOTE_START SCALAR DOUBLEQUOTE_END
        """
        scalar = re.sub('\n\s+', ' ', str(p[2]))
        p[0] = Str(scalar)

    @strict(Str)
    def p_scalar_singlequote(self, p):
        """
        scalar  : SINGLEQUOTE_START SCALAR SINGLEQUOTE_END
        """
        p[0] = Str(str(p[2]).replace("''", "'"))

    @strict(Str)
    def p_scalar_quote_empty(self, p):
        """
        scalar  : DOUBLEQUOTE_START DOUBLEQUOTE_END
                | SINGLEQUOTE_START SINGLEQUOTE_END
        """
        p[0] = Str('')

    @strict(Scalar)
    def p_scalar_explicit_cast(self, p):
        """
        scalar  : CAST_TYPE scalar
        """
        p[0] = ScalarDispatch(p[2].raw_value, cast=p[1])

    @strict(Scalar)
    def p_scalar(self, p):
        """
        scalar  : SCALAR
        """
        p[0] = ScalarDispatch(p[1])

    @strict(Str)
    def p_scalar_literal(self, p):
        """
        scalar  : B_LITERAL_START scalar_group B_LITERAL_END
        """
        scalar_group = ''.join(p[2])
        p[0] = ScalarDispatch(dedent(scalar_group).rstrip('\n').replace('\n\n\n', '\n'), cast='str')

    @strict(Str)
    def p_scalar_folded(self, p):
        """
        scalar  : B_FOLD_START scalar_group B_FOLD_END
        """
        scalar_group = ''.join(p[2])
        cleaned_scalar = fold(dedent(scalar_group).rstrip('\n'))
        p[0] = ScalarDispatch(cleaned_scalar, cast='str')

    @strict(Str)
    def p_scalar_indented_flow(self, p):
        """
        scalar  : INDENT scalar_group DEDENT
        """
        scalar_group = '\n'.join(p[2])
        cleaned_scalar = fold(dedent(scalar_group).rstrip('\n'))
        p[0] = ScalarDispatch(cleaned_scalar, cast='str')

    @strict(tuple)
    def p_scalar_group(self, p):
        """
        scalar_group    : SCALAR
                        | scalar_group SCALAR
        """
        if len(p) == 2:
            p[0] = (str(p[1]),)

        if len(p) == 3:
            p[0] = p[1] + (str(p[2]),)

    @strict(Sequence, Map)
    def p_flow_collection(self, p):
        """
        flow_collection : F_SEQUENCE_START flow_sequence F_SEQUENCE_END
                        | F_MAP_START flow_map F_MAP_END
        """
        p[0] = p[2]

    @strict(Sequence)
    def p_flow_sequence_last(self, p):
        """
        flow_sequence   : flow_sequence_item
        """
        p[0] = Sequence(p[1])

    @strict(Sequence)
    def p_flow_sequence_init(self, p):
        """
        flow_sequence   : flow_sequence F_SEP flow_sequence_item
        """
        p[0] = p[1] + Sequence(p[3])

    @strict(Scalar)
    def p_flow_sequence_item(self, p):
        """
        flow_sequence_item  : scalar
        """
        p[0] = p[1]

    @strict(Map)
    def p_flow_map_last(self, p):
        """
        flow_map   : flow_map_item
        """
        p[0] = Map(p[1])

    @strict(Map)
    def p_flow_map_init(self, p):
        """
        flow_map   : flow_map F_SEP flow_map_item
        """
        p[0] = p[1] + Map(p[3])

    @strict(tuple)
    def p_flow_map_item(self, p):
        """
        flow_map_item  : flow_map_item_key flow_map_item_value
        """
        p[0] = p[1], p[2]

    @strict(Scalar)
    def p_flow_map_item_key(self, p):
        """
        flow_map_item_key   : scalar F_MAP_KEY
        """
        p[0] = p[1]

    @strict(Scalar)
    def p_flow_map_item_value(self, p):
        """
        flow_map_item_value    : scalar
        """
        p[0] = p[1]

    def p_empty(self, p):
        """empty    :"""
        pass
