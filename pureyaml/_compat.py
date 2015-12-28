# coding=utf-8
"""Python 2to3 compatibility handling."""

import logging

try:
    from logging import NullHandler
except ImportError:  # pragma: no cover
    # Python < 2.7
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
