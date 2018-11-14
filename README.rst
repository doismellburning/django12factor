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

"`The Twelve-Factor App <https://12factor.net/>`__\ " is an awesome
methodology for building SaaS apps.

``django-12factor`` makes Django more 12factor-y. Right now, this
focuses on the `Config <https://12factor.net/config>`__ - "Store config
in the environment"; `Heroku <https://www.heroku.com/>`__ users with
addons will be particularly familiar with this.

Still not sure of the benefits? Check out
"`Twelve-Factor Config: Misunderstandings and Advice <https://blog.doismellburning.co.uk/2014/10/06/twelve-factor-config-misunderstandings-and-advice/>`__".

Documentation
-------------

https://django12factor.readthedocs.org/en/latest/

Licensing
---------

django12factor is licensed under the terms of the MIT License (see
`License <LICENSE>`__).

django12factor includes copies of Python's ``captured_output``,
``captured_stdout`` and ``captured_stderr`` context managers, which are
licensed under the terms of the
`PSF LICENSE AGREEMENT FOR PYTHON <https://docs.python.org/3/license.html>`__.

Credits
-------

Originally written by Kristian Glass / @doismellburning, now maintained by the
wonderful Jonas Maurus / @jdelic
