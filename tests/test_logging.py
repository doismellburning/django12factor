from __future__ import (
    absolute_import,
    print_function,
)

from contextlib import contextmanager

import six
import django12factor
import logging
import logging.config
import sys
import unittest

from .env import env

debug_env = env(DEBUG="1", SECRET_KEY="secret")


def has_handler(logger, handler_name):
    return any([handler.name == handler_name for handler in logger.handlers])


# Vendored in version of Python's
# https://docs.python.org/3.5/library/test.html#module-test
@contextmanager
def captured_output(stream_name):
    """Return a context manager used by captured_stdout/stdin/stderr
    that temporarily replaces the sys stream *stream_name* with a StringIO.

    Note: This function and the following ``captured_std*`` are copied
          from CPython's ``test.support`` module."""
    orig_stdout = getattr(sys, stream_name)
    setattr(sys, stream_name, six.StringIO())
    try:
        yield getattr(sys, stream_name)
    finally:
        setattr(sys, stream_name, orig_stdout)


def captured_stdout():
    """Capture the output of sys.stdout:

       with captured_stdout() as stdout:
           print("hello")
       self.assertEqual(stdout.getvalue(), "hello\n")
    """
    return captured_output("stdout")


def captured_stderr():
    """Capture the output of sys.stderr:

       with captured_stderr() as stderr:
           print("hello", file=sys.stderr)
       self.assertEqual(stderr.getvalue(), "hello\n")
    """
    return captured_output("stderr")


class TestLogging(unittest.TestCase):

    def test_root_logger_config(self):
        """
        Assert basic expectations about the root logger.

        Due to a misreading of
        https://docs.python.org/2/library/logging.config.html#dictionary-schema-details,
        d12f was at one point configuring a logger named "root", rather than
        the actual root logger. This was obviously mildly suboptimal.

        This test makes more assumptions than ideal about how the desired root
        config.
        """
        with debug_env:
            logging.config.dictConfig(django12factor.factorise()["LOGGING"])
            self.assertTrue(has_handler(logging.root, "stdout"))

    def test_capture_stdout_works_with_print(self):
        """
        Assert that `capture_stdout` captures `print` text
        """
        with debug_env:
            with captured_stdout() as stdout:
                print("wibble")

        self.assertIn("wibble", stdout.getvalue())

    def test_logging_to_stdout(self):
        with debug_env:
            with captured_stdout() as stdout:
                logging.config.dictConfig(django12factor.factorise()["LOGGING"])
                message = "lorem ipsum"
                logging.info(message)

        output = stdout.getvalue()
        self.assertIn(
            message, output,
            "Message '%s' should have been logged to stdout and captured;"
            "instead '%s' was captured" % (message, output)
        )
