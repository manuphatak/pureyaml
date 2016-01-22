#!/usr/bin/env python
# coding=utf-8

import logging

import sys

from tests.utils import test_dir, PY26, PY27, PY33, PY34, PY35, PYPY

version = {  # :off
    PY26: 'PY26',
    PY27: 'PY27',
    PY33: 'PY33',
    PY34: 'PY34',
    PY35: 'PY35',
    PYPY: 'PYPY',
}  # :on


def init_logger():
    # FORMATTERS
    # ------------------------------------------------------------------------
    message_formatter = logging.Formatter('%(message)s')
    simple_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # HANDLERS
    # ------------------------------------------------------------------------
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(message_formatter)
    stderr_handler.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(message_formatter)
    stdout_handler.setLevel(logging.WARNING)

    filename = test_dir('logs', '%s_pureyaml.log' % version[True].lower())
    file_handler = logging.FileHandler(filename, mode='w', encoding='utf-8')
    file_handler.setFormatter(simple_formatter)
    file_handler.setLevel(logging.DEBUG)

    filename = test_dir('logs', '%s_pureyaml_ply.log' % version[True].lower())
    ply_file_handler = logging.FileHandler(filename, mode='w', encoding='utf-8')
    ply_file_handler.setFormatter(simple_formatter)
    ply_file_handler.setLevel(logging.DEBUG)

    # LOGGERS
    # ------------------------------------------------------------------------
    pureyaml_logger = logging.getLogger('pureyaml')
    pureyaml_logger.addHandler(stdout_handler)
    pureyaml_logger.addHandler(stderr_handler)
    pureyaml_logger.addHandler(file_handler)
    pureyaml_logger.setLevel(logging.DEBUG)
    pureyaml_logger.propagate = True

    lex_logger = logging.getLogger('pureyaml.ply.lex')
    lex_logger.addHandler(ply_file_handler)
    lex_logger.setLevel(logging.DEBUG)
    lex_logger.propagate = True

    yacc_logger = logging.getLogger('pureyaml.ply.yacc')
    yacc_logger.addHandler(ply_file_handler)
    yacc_logger.setLevel(logging.DEBUG)
    yacc_logger.propagate = True
