"""
Utility class for transforming environment variables into Django settings.
"""

import os


def identity(x):
    """
    Because Python's stdlib doesn't have an identity function.
    """

    return x


class EnvironmentVariableLoader(object):
    """
    Load an environment variable, for a flexible value of load.

    Provide an (optional) parser function (e.g. `int`), and an (optional) default.
    """

    def __init__(self, name, default=None, parser=identity):
        """
        Build a loader for an environment variable.

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
        """
        Load and process an environment variable.
        """

        if self.name in os.environ:
            return self.parser(os.environ[self.name])
        else:
            return self.default


EVL = EnvironmentVariableLoader
