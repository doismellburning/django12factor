from __future__ import absolute_import

import django12factor
import unittest
import django

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

    def test_debug_defaults_to_off(self):
        """
        Ensure that by default, DEBUG is false (for safety reasons)
        """
        with env(SECRET_KEY="x"):
            self.assertFalse(d12f()['DEBUG'])

    def test_template_debug(self):
        # for this test, we pretend to be Django < 1.8
        oldversion = django.VERSION
        django.VERSION = (1, 7, 0, "test_template_debug", 1)
        with debugenv():
            # Unless explicitly set, TEMPLATE_DEBUG = DEBUG
            self.assertTrue(d12f()['TEMPLATE_DEBUG'])

        with debugenv(TEMPLATE_DEBUG="false"):
            s = d12f()
            self.assertFalse(s['TEMPLATE_DEBUG'])
            self.assertTrue(s['DEBUG'])
        django.VERSION = oldversion

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

    def test_multiple_db_support(self):
        """
        Explicit test that multiple DATABASE_URLs are supported.

        https://github.com/doismellburning/django12factor/issues/36 turned out
        to be due to using an incorrect version of the library, BUT it made me
        realise that there was no explicit test for multiple named databases.
        So this is one.
        """
        e = {
            "CLIENT_DATABASE_URL": "mysql://root@127.0.0.1:3306/apps",
            "DATABASE_URL": "mysql://root@127.0.0.1:3306/garage",
            "BRD_DATABASE_URL": "mysql://root@127.0.0.1:3306/brd",
        }

        with debugenv(**e):
            dbs = d12f()['DATABASES']

            self.assertEquals(len(dbs), 3)

    def test_named_db_support(self):
        DBNAME = "test"
        DB_URL_NAME = "%s_DATABASE_URL" % DBNAME.upper()
        e = {DB_URL_NAME: "postgres://username:password@host:1234/dbname"}

        with debugenv(**e):
            dbs = d12f()['DATABASES']
            self.assertIn(
                'sqlite',
                dbs['default']['ENGINE'],
                "Failed to load default DATABASE"
            )
            self.assertIn(
                DBNAME,
                dbs,
                "Failed to parse a database called '%s' from the environment "
                "variable %s" % (DBNAME, DB_URL_NAME)
            )
            self.assertIn('postgres', dbs[DBNAME]['ENGINE'])

    def test_multiple_default_databases(self):
        """
        Ensure if DEFAULT_DATABASE_URL and DATABASE_URL are set, latter wins.
        """

        IGNORED_DB_NAME = "should_be_ignored"
        DATABASE_URL = "postgres://username:password@host:1234/dbname"
        IGNORED = "postgres://username:password@host:1234/%s" % IGNORED_DB_NAME

        with debugenv(DATABASE_URL=DATABASE_URL, DEFAULT_DATABASE_URL=IGNORED):
            default_db = d12f()['DATABASES']['default']
            self.assertNotEquals(
                default_db['NAME'],
                IGNORED_DB_NAME,
                "Parsed the contents of DEFAULT_DATABASE_URL instead of "
                "ignoring it in favour of DATABASE_URL"
            )

    def test_non_capitalised_database_ignored(self):
        """
        Ensure "malformed" X_DATABASE_URLs aren't parsed.
        """

        e = {
            'invalid_DATABASE_URL': "",
            'AlsoInValid_DATABASE_URL': "",
            'ALMOST_CORRECt_DATABASE_URL': "",
        }

        with debugenv(**e):
            dbs = d12f()['DATABASES']

            self.assertEquals(
                len(dbs),
                1,
                "Loaded %d databases instead of just 1 (default) - got %s "
                "from environment %s" % (len(dbs), dbs.keys(), e)
            )

    def test_use_x_forwarded_proto(self):
        with debugenv(TRUST_X_FORWARDED_PROTO="on"):
            settings = d12f()
            self.assertEquals(('HTTP_X_FORWARDED_PROTO', 'https'), settings['SECURE_PROXY_SSL_HEADER'])

        with debugenv(TRUST_X_FORWARDED_PROTO="off"):
            settings = d12f()
            self.assertEquals(None, settings['SECURE_PROXY_SSL_HEADER'])
