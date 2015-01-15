import django12factor
import unittest

from .env import (
    debugenv,
)
from django12factor.environment_variable_loader import EVL

d12f = django12factor.factorise


class TestEVL(unittest.TestCase):

    def test_equivalence(self):
        with debugenv(FOO='x'):
            custom_string = d12f(custom_settings=['FOO'])

        with debugenv(FOO='x'):
            custom_evl = d12f(custom_settings=[EVL("FOO")])

        self.assertEqual(custom_string, custom_evl)
