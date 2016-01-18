#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

import os
import sys

from pytest import mark


def test_dir(*paths):
    dirname = os.path.dirname(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(dirname, *paths))


feature_not_supported = mark.skipif(True, reason='Feature not supported.')

PY33 = sys.version_info[0:2] == (3, 3)
PY34 = sys.version_info[0:2] == (3, 4)
PY35 = sys.version_info[0:2] == (3, 5)
