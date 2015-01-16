import os


class EnvironmentVariableLoader(object):
    def __init__(self, name, default=None, **kwargs):
        self.name = name
        self.default = default

    def load_value(self):
        return os.getenv(self.name, default=self.default)


EVL = EnvironmentVariableLoader
