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

    def test_default_is_none(self):
        with debugenv():
            key = "FOO"
            d = d12f(custom_settings=[EVL(key)])
            self.assertIsNone(
                d[key],
                "d12f tried to load the (unset) environment variable '%s' "
                "with no default; expected None but got %s instead" %
                (key, str(d[key]))
            )

    def test_custom_default(self):
        with debugenv():
            key = "FOO"
            default = "llama"
            d = d12f(custom_settings=[EVL(key, default=default)])
            self.assertEquals(
                default, d[key],
                "d12f tried to load the (unset) environment variable '%s' "
                "with a default of %s, but got %s instead" %
                (key, str(default), str(d[key]))
            )
