"""
django12factor: Bringing 12factor configuration to Django.

* https://12factor.net/
* https://12factor.net/config
* https://github.com/doismellburning/django12factor
"""

import django_cache_url
import dj_database_url
import dj_email_url
import django
import os
import logging
import six
import sys

logger = logging.getLogger(__name__)

_FALSE_STRINGS = [
    "no",
    "false",
    "off",
]


def getenv_bool(setting_name):
    """
    Get a boolean from an environment variable.

    Why use this and not just `bool(os.getenv("X"))`?  It would be quite
    reasonable to see `DEBUG=true`, and infer that setting `DEBUG=false` would
    Do The Right Thing; however `bool("false") == True`.

    This function attempts to do basic "is the string falsey" detection so
    `DEBUG=false` behaves as expected
    """

    if setting_name not in os.environ:
        return False

    var = os.environ[setting_name]

    return not (var.lower() in _FALSE_STRINGS)


def factorise(custom_settings=None):
    """
    Return a dict of settings for Django, acquired from the environment.

    This is done in a 12factor-y way - see https://12factor.net/config

    Caller probably wants to, in `settings.py`:

    globals().update(factorise())
    """

    settings = {}

    settings['LOGGING'] = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'stdout': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            }
        },
        'root': {
            'handlers': ['stdout'],
        },
    }

    settings['DATABASES'] = {
        'default': dj_database_url.config(default='sqlite://:memory:')
    }

    for (key, value) in six.iteritems(os.environ):
        _SUFFIX = "_DATABASE_URL"
        _OFFSET = len(_SUFFIX)

        if key.endswith(_SUFFIX):
            prefix = key[:-_OFFSET]

            if not prefix.isupper():
                # i.e. it was not already all upper-cased
                logger.warning(
                    "Not parsing %s as a database url because the "
                    "prefix (%s) was not all upper-case - django12factor "
                    "will convert prefixes to lower-case for use as database "
                    "names", key, prefix)
                continue

            dbname = key[:-_OFFSET].lower()

            if dbname == "default" and 'DATABASE_URL' in os.environ:
                logger.warning(
                    "You have set the environment variables DATABASE_URL "
                    "_and_ %s, both of which would configure "
                    "`DATABASES['default']`. {key} is being "
                    "ignored.", key)
                continue

            db = dj_database_url.parse(value)
            settings['DATABASES'][dbname] = db

    settings['DEBUG'] = getenv_bool('DEBUG')
    if django.VERSION < (1, 8):
        if 'TEMPLATE_DEBUG' in os.environ:
            settings['TEMPLATE_DEBUG'] = getenv_bool('TEMPLATE_DEBUG')
        else:
            settings['TEMPLATE_DEBUG'] = settings['DEBUG']

    # Slightly opinionated...
    if 'SECRET_KEY' in os.environ:
        settings['SECRET_KEY'] = os.environ['SECRET_KEY']
    elif not settings['DEBUG']:
        sys.exit("""DEBUG is False but no SECRET_KEY is set in the environment -
either it has been hardcoded (bad) or not set at all (bad) - exit()ing for
safety reasons""")
    else:
        settings['SECRET_KEY'] = 'debugkey'

    settings['CACHES'] = {
        'default': django_cache_url.config(default='locmem://')
    }

    settings.update(dj_email_url.config(default='dummy://'))

    settings['ALLOWED_HOSTS'] = os.getenv('ALLOWED_HOSTS', '').split(',')

    # For keys to different apis, etc.
    if custom_settings is None:
        custom_settings = []

    for cs in custom_settings:
        settings[cs] = os.getenv(cs)

    return settings
