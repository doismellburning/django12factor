# django-12factor

## What is it?

[Django](https://www.djangoproject.com/) is an awesome Python web framework.

"[The Twelve-Factor App](http://12factor.net/)" is an awesome methodology for building SaaS apps.

`django-12factor` makes Django more 12factor-y. Right now, this focuses on the [Config](http://12factor.net/config) - "Store config in the environment"; [Heroku](http://www.heroku.com/) users with addons will be particularly familiar with this.

## Usage

Add the following to the bottom of your `settings.py`:

    import django12factor
    d12f = django12factor.factorise()

`factorise()` returns a `dict` of settings, so you can now use and assign them as you wish, e.g.

    DEBUG = d12f['DEBUG']
    LOGGING = d12f['LOGGING']

If you don't like that repetition, you can (ab)use `globals()` like so:

    import django12factor
    d12f = django12factor.factorise()

    def f(setting):
        globals()[setting] = d12f[setting]

    f('DEBUG')
    f('LOGGING')

### Give me everything!

If you say so...

    import django12factor
    globals().update(django12factor.factorise())

## Settings

The following settings are currently supported:

### `DEBUG`

### `TEMPLATE_DEBUG`

### `CACHES`

Uses [`django-cache-url`](https://github.com/ghickman/django-cache-url)

### `LOGGING`

### `DATABASES`

Uses [`dj-database-url`](https://github.com/kennethreitz/dj-database-url)

### `ALLOWED_HOSTS`

### `SECRET_KEY`
