import dj_database_url
import uuid
import os
import logging

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

    # Slightly opinionated...
    if 'SECRET_KEY' in os.environ:
        settings['SECRET_KEY'] = os.environ['SECRET_KEY']
    else:
        logger.warn('No SECRET_KEY provided, using UUID')
        settings['SECRET_KEY'] = uuid.uuid4()

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
        'default': dj_database_url.config(default='sqlite://:memory:') # Note this'll currently break due to https://github.com/kennethreitz/dj-database-url/pull/21
    }

    settings['DEBUG'] = getenv_bool('DEBUG')
    if 'TEMPLATE_DEBUG' in os.environ:
        settings['TEMPLATE_DEBUG'] = getenv_bool('TEMPLATE_DEBUG')
    else:
        settings['TEMPLATE_DEBUG'] = settings['DEBUG']

    return settings
