# coding=utf-8
"""Python 2to3 compatibility handling."""

try:
    from logging import NullHandler
except ImportError:  # pragma: no cover
    import logging


    class NullHandler(logging.Handler):  # Python < 2.7
        def emit(self, record):
            pass
