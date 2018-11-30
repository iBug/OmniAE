# LOL. Hope you're not fooled by the name of this file


import os
from configparser import ConfigParser


# Note: All classes here have N801 (CapWords naming convention) disabled.
# They're intended to be singletons


class config:  # noqa: N801
    read_key = None
    write_key = None
    write_token = None


config_parser = ConfigParser()


def load():
    global config_parser

    if os.path.isfile("config"):
        config_parser.read("config", encoding="utf-8")
    else:
        config_parser.read("config.sample", encoding="utf-8")

    conf = config_parser['Config']
