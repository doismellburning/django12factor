import os


class Env(object):
    """
    Test helper providing temporary environments.

    Usage:

        with Env(DEBUG="true"):
            d = django12factor.factorise()
    """

    def __init__(self, **kwargs):
        self.environ = kwargs

    def __enter__(self):
        self.oldenviron = os.environ
        os.environ = self.environ

    def __exit__(self, type, value, traceback):
        os.environ = self.oldenviron

env = Env
