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

    def test_databases(self):
        with env(DEBUG="true", DATABASES="postgres://username:password@host:1234/dbname"):
            self.assertEqual(
                d12f()['DATABASES']['ENGINE'], 'django.db.backends.postgresql_psycopg2')
            self.assertEqual(
                d12f()['DATABASES']['NAME'], 'dbname')

class Env(object):
    def __init__(self, **kwargs):
        self.environ = kwargs

    def __enter__(self):
        self.oldenviron = os.environ
        os.environ = self.environ

    def __exit__(self, type, value, traceback):
        os.environ = self.oldenviron

env = Env
