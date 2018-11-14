# Changelog

## Unreleased

* Dropped Python 3.2 and 3.3 support
* Added Python 3.5, 3.6, 3.7 support
* Treat `0` as `false` in boolean settings.
* Removed pinning of library versions in `install_requires`
* Added new maintainer @jdelic
* Vendored Python 3's `captured_output` contextmanager for tests
* Switched from deprecated `warning()` to `warn()`
* Added PEP484 annotations as .pyi file
* Updated all dependencies

>>>>>>> Stashed changes

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
