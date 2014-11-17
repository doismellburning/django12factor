from __future__ import (
    absolute_import,
    print_function,
)

import StringIO
import django12factor
import logging
import logging.config
import sys
import unittest

from .env import env

debug_env = env(DEBUG="1", SECRET_KEY="secret")


def has_handler(logger, handler_name):
    return any([handler.name == handler_name for handler in logger.handlers])


def capture_stdout(command, *args, **kwargs):
    normal_stdout = sys.stdout
    captured_stdout = StringIO.StringIO()
    sys.stdout = captured_stdout

    command(*args, **kwargs)

    captured_stdout.seek(0)
    return captured_stdout.read()

    sys.stdout = normal_stdout


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
            logging.config.dictConfig(django12factor.factorise()['LOGGING'])
            self.assertTrue(has_handler(logging.root, "stdout"))

    def test_logging_to_stdout(self):

        with debug_env:
            logging.config.dictConfig(django12factor.factorise()['LOGGING'])

            output = capture_stdout(print, "wibble")
            self.assertIn("wibble", output)

            message = "lorem ipsum"
            output = capture_stdout(logging.info, message)
            self.assertIn(message, output, "Message '%s' should have been logged to stdout and captured; instead '%s' was captured" % (message, output))
