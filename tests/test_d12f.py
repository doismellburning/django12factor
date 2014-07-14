import django12factor
import os
import unittest

d12f = django12factor.factorise

class TestD12F(unittest.TestCase):

    def test_object_no_secret_key_prod(self):
        with env(DEBUG="false"):
            self.assertRaises(SystemExit, d12f)

    def test_debug(self):
        with env(DEBUG="true"):
            self.assertTrue(d12f()['DEBUG'])

    def test_db(self):
        with env(DEBUG="true"):
            self.assertIn("sqlite", d12f()['DATABASES']['default']['ENGINE'])

        with env(DEBUG="true", DATABASE_URL="sqlite://:memory:"):
            self.assertIn("sqlite", d12f()['DATABASES']['default']['ENGINE'])

        with env(DEBUG="true", DATABASE_URL="postgres://username:password@host:1234/dbname"):
            db = d12f()['DATABASES']['default']
            self.assertIn("postgres", db['ENGINE'])
            self.assertEquals("dbname", db['NAME'])


class Env(object):
    def __init__(self, **kwargs):
        self.environ = kwargs

    def __enter__(self):
        self.oldenviron = os.environ
        os.environ = self.environ

    def __exit__(self, type, value, traceback):
        os.environ = self.oldenviron

env = Env
