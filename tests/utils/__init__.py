#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

import os
import sys

from future.utils import PY26 as _PY26, PY27 as _PY27, PY2 as _PY2, PY3 as _PY3, PYPY as _PYPY
from pytest import mark


def test_dir(*paths):
    dirname = os.path.dirname(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(dirname, *paths))


feature_not_supported = mark.xfail(True, reason='Feature not supported.')

PY2 = _PY2
PY3 = _PY3
PY26 = _PY26 and not _PYPY
PY27 = _PY27 and not _PYPY
PYPY = _PYPY
PY33 = sys.version_info[0:2] == (3, 3)
PY34 = sys.version_info[0:2] == (3, 4)
PY35 = sys.version_info[0:2] == (3, 5)


from .logger import init_logger
from .multi_test_case import MultiTestCaseBase
from .node_diff import get_node_diff
from .parametrized_tests_data import ParametrizedTestData
from .serialize_nodes import serialize_nodes

__all__ = [  # :off
        'test_dir',
        'feature_not_supported',
        'PY2',
        'PY3',
        'PY26',
        'PY27',
        'PYPY',
        'PY33',
        'PY34',
        'PY35',
        'init_logger',
        'get_node_diff',
        'ParametrizedTestData',
        'serialize_nodes',
        'MultiTestCaseBase'
    ]  # :on
