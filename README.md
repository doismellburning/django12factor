# django-12factor

## What is it?

[Django](https://www.djangoproject.com/) is an awesome Python web framework.

"[The Twelve-Factor App](http://12factor.net/)" is an awesome methodology for building SaaS apps.

`django-12factor` makes Django more 12factor-y. Right now, this focuses on the [Config](http://12factor.net/config) - "Store config in the environment"; [Heroku](http://www.heroku.com/) users with addons will be particularly familiar with this.

## Usage

Add the following to the bottom of your `settings.py`:

    from django12factor import factorise
    globals().update(factorise())

### But I don't want everything django12factor provides!

`factorise()` returns a `dict` of settings, so controlling what elements of `django12factor` you use is easy:

### Whitelisting

    from django12factor import factorise
    d12f = factorise()
    DEBUG = d12f['DEBUG']
    LOGGING = d12f['LOGGING']
    # ...

### Blacklisting

    from django12factor import factorise
    d12f = factorise()
    del d12f['SECRET_KEY']
    # ...
    globals().update(d12f)

