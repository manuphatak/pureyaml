# coding=utf-8
"""Python 2to3 compatibility handling."""

try:
    from logging import NullHandler
except ImportError:  # pragma: no cover
    import logging  # :off

    # Python < 2.7
    class NullHandler(logging.Handler):  # :on
        def emit(self, record):
            pass
