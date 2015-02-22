django-12factor
===============

.. image:: https://travis-ci.org/doismellburning/django12factor.svg?branch=master
       :target: https://travis-ci.org/doismellburning/django12factor

.. image:: https://landscape.io/github/doismellburning/django12factor/master/landscape.png
       :target: https://landscape.io/github/doismellburning/django12factor/master
       :alt: Code Health

.. image:: https://requires.io/github/doismellburning/django12factor/requirements.svg?branch=master
       :target: https://requires.io/github/doismellburning/django12factor/requirements/?branch=master
       :alt: Requirements Status

.. image:: https://coveralls.io/repos/doismellburning/django12factor/badge.svg
       :target: https://coveralls.io/r/doismellburning/django12factor
       :alt: Coverage Status

What is it?
-----------

`Django <https://www.djangoproject.com/>`__ is an awesome Python web
framework.

"`The Twelve-Factor App <http://12factor.net/>`__\ " is an awesome
methodology for building SaaS apps.

``django-12factor`` makes Django more 12factor-y. Right now, this
focuses on the `Config <http://12factor.net/config>`__ - "Store config
in the environment"; `Heroku <http://www.heroku.com/>`__ users with
addons will be particularly familiar with this.

Still not sure of the benefits? Check out
"`Twelve-Factor Config: Misunderstandings and Advice <http://blog.doismellburning.co.uk/2014/10/06/twelve-factor-config-misunderstandings-and-advice/>`__".

Usage
-----

Add the following to the bottom of your ``settings.py``:

.. code-block:: python

    import django12factor
    d12f = django12factor.factorise()

``factorise()`` returns a ``dict`` of settings, so you can now use and
assign them as you wish, e.g.

.. code-block:: python

    DEBUG = d12f['DEBUG']
    LOGGING = d12f['LOGGING']

If you don't like that repetition, you can (ab)use ``globals()`` like
so:

.. code-block:: python

    import django12factor
    d12f = django12factor.factorise()

    def f(setting):
        globals()[setting] = d12f[setting]

    f('DEBUG')
    f('LOGGING')

You can also add non-Django settings this way, e.g. keys to APIs:

.. code-block:: python

    custom_settings = (
        "GOOGLE_ANALYTICS_KEY",
        "MAILCHIMP_API_KEY",
    )
    d12f = django12factor.factorise(custom_settings=custom_settings)

    MAILCHIMP_API_KEY = d12f['MAILCHIMP_API_KEY']
    GOOGLE_ANALYTICS_KEY = d12f['GOOGLE_ANALYTICS_KEY']

In the event of a ``custom_setting`` not being set in the environment, it will
default to ``None``.

Give me everything!
~~~~~~~~~~~~~~~~~~~

If you say so...

.. code-block:: python

    import django12factor
    globals().update(django12factor.factorise())

Utilities
---------

``django12factor.getenv_bool`` is a utility function that takes the name of an
environment variable, and returns ``True`` _unless_ it is set to either a
"falsey" string (e.g. ``"no"``) or not set.

Settings
--------

The following settings are currently supported:

``DEBUG``
~~~~~~~~~

Defaults to ``False`` for safety reasons, otherwise ``True`` unless
``os.environ("DEBUG")`` is a "falsy" string.

``TEMPLATE_DEBUG``
~~~~~~~~~~~~~~~~~~

As for ``DEBUG``, but defaults to the value of ``DEBUG``.

``CACHES``
~~~~~~~~~~

Uses
`django-cache-url <https://github.com/ghickman/django-cache-url>`__ to parse ``os.environ("CACHE_URL")``.

``LOGGING``
~~~~~~~~~~~

A static ``LOGGING`` dict that configures `12factor-style logging <http://12factor.net/logs>`__.

``DATABASES``
~~~~~~~~~~~~~

Uses
`dj-database-url <https://github.com/kennethreitz/dj-database-url>`__ -
parses ``DATABASE_URL`` if it exists, otherwise falls back to in-memory sqlite.

Anything of the form ``FOO_DATABASE_URL`` will be parsed as
``DATABASES['foo']``, allowing you to configure multiple databases via the
environment.

``ALLOWED_HOSTS``
~~~~~~~~~~~~~~~~~

Treats ``os.environ("ALLOWED_HOSTS")`` as a comma-separated list.

``SECRET_KEY``
~~~~~~~~~~~~~~

Uses ``os.environ("SECRET_KEY")`` - required if ``DEBUG==False``.
