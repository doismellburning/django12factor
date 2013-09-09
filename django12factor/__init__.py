import django_cache_url
import dj_database_url
import dj_email_url
import os
import logging
import sys

logger = logging.getLogger(__name__)

_FALSE_STRINGS = [
    "no",
    "false",
    "off",
]

def getenv_bool(setting_name):
    if setting_name not in os.environ:
        return False

    var = os.environ[setting_name]

    return not (var.lower() in _FALSE_STRINGS)


def factorise():
    """
    Returns a dict of settings suitable for Django, acquired from the environment in a 12factor-y way - see http://12factor.net/config

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
        'loggers': {
            'root': {
                'handlers': ['stdout'],
                'propagate': True,
            },
        },
    }

    settings['DATABASES'] = {
        'default': dj_database_url.config(default='sqlite://:memory:')
    }

    settings['DEBUG'] = getenv_bool('DEBUG')
    if 'TEMPLATE_DEBUG' in os.environ:
        settings['TEMPLATE_DEBUG'] = getenv_bool('TEMPLATE_DEBUG')
    else:
        settings['TEMPLATE_DEBUG'] = settings['DEBUG']

    # Slightly opinionated...
    if 'SECRET_KEY' in os.environ:
        settings['SECRET_KEY'] = os.environ['SECRET_KEY']
    elif not settings['DEBUG']:
        sys.exit('DEBUG is False but no SECRET_KEY is set in the environment - either it has been hardcoded (bad) or not set at all (bad) - exit()ing for safety reasons')

    settings['CACHES'] = {
        'default': django_cache_url.config(default='locmem://')
    }

    settings.update(dj_email_url.config(default='dummy://'))

    settings['ALLOWED_HOSTS'] = os.getenv('ALLOWED_HOSTS', '').split(',')

    return settings
