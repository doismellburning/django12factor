import os


class Env(object):
    def __init__(self, **kwargs):
        self.environ = kwargs

    def __enter__(self):
        self.oldenviron = os.environ
        os.environ = self.environ

    def __exit__(self, type, value, traceback):
        os.environ = self.oldenviron


def debugenv(**kwargs):
    return env(DEBUG="true", **kwargs)


env = Env
