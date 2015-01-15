from __future__ import absolute_import

import django12factor
import unittest

from .env import env

d12f = django12factor.factorise


def debugenv(**kwargs):
    return env(DEBUG="true", **kwargs)


class TestD12F(unittest.TestCase):

    def test_object_no_secret_key_prod(self):
        with env(DEBUG="false"):
            self.assertRaises(SystemExit, d12f)

    def test_debug(self):
        with debugenv():
            self.assertTrue(d12f()['DEBUG'])

    def test_db(self):
        with debugenv():
            self.assertIn("sqlite", d12f()['DATABASES']['default']['ENGINE'])

        with debugenv(DATABASE_URL="sqlite://:memory:"):
            self.assertIn("sqlite", d12f()['DATABASES']['default']['ENGINE'])

        postgenv = debugenv(
            DATABASE_URL="postgres://username:password@host:1234/dbname",
        )
        with postgenv:
            db = d12f()['DATABASES']['default']
            self.assertIn("postgres", db['ENGINE'])
            self.assertEquals("dbname", db['NAME'])

    def test_custom_key(self):
        with debugenv(CUSTOM_KEY="banana"):
            settings = d12f(['CUSTOM_KEY'])
            self.assertIn("banana", settings['CUSTOM_KEY'])

    def test_missing_custom_keys(self):
        present = 1
        with debugenv(PRESENT=present):
            settings = d12f(['PRESENT', 'MISSING'])
            self.assertEquals(present, settings['PRESENT'])
            self.assertIsNone(settings['MISSING'])
