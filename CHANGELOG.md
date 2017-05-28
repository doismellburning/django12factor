# Changelog

## Unreleased

* Dropped Python 3.2 support
* Use sqlite:///db.sqlite3 as the default DATABASE_URL

## 1.3

* Python 3.2 and 3.4 support
* Improved test suite - 100% coverage + flake8
* Multiple database support - `TEST_DATABASE_URL` will create `settings.DATABASES['test']`

## 1.2

* Update dependencies

## 1.1

* Grab arbitrary environment variables as settings with the `custom_settings` parameter

## 1.0

* Initial public release
* Supported environment variables:
    * DEBUG
    * TEMPLATE_DEBUG
    * CACHES (using django-cache-url)
    * LOGGING
    * DATABASES (using dj-database-url)
    * ALLOWED_HOSTS
    * SECRET_KEY
