# LOL. Hope you're not fooled by the name of this file


import os
from configparser import ConfigParser


class config:  # noqa: N801
    parser = ConfigParser()

    @classmethod
    def load(cls):
        if os.path.isfile("config"):
            cls.parser.read("config")
        else:
            cls.parser.read("config.default")
