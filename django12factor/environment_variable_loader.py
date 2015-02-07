import os


def identity(x):
    return x


class EnvironmentVariableLoader(object):
    def __init__(self, name, default=None, parser=identity):
        """
        Builds a loader for an environment variable.

        * `name`: (required) the environment key to use
        * `default`: a value to use if the environment variable is not set
        * `loader`: a function that takes a string environment value and
          performs type conversion / parsing / etc. (e.g. `int` or
          `lambda x: x.split(',')`)

        Note there is no checking to ensure the type of `default` is the same
        as the return type of `loader`, but if this isn't the case, you're
        probably going to have a sad time.
        """
        self.name = name
        self.default = default
        self.parser = parser

    def load_value(self):
        if self.name in os.environ:
            return self.parser(os.environ[self.name])
        else:
            return self.default


EVL = EnvironmentVariableLoader
