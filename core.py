# LOL. Hope you're not fooled by the name of this file


import sys
import os
from configparser import ConfigParser


# Note: All classes here have N801 (CapWords naming convention) disabled.
# They're intended to be singletons


class Object(object):
    def __init__(self, _default=None, **kwargs):
        self.__dict__["_data"] = dict(kwargs)
        self.__dict__["_default"] = _default

    def __getattr__(self, attr):
        try:
            return self._data[attr]
        except KeyError:
            if self._default:
                self._data[attr] = self._default()
                return self._data[attr]
            raise AttributeError("Object has no attribute {!r}".format(attr)) from None

    def __setattr__(self, attr, value):
        self._data[attr] = value
        return value

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value
        return value

    def set_default(self, default=None):
        if default is True:
            default = Object
        self._default = default


config = Object(_default=type(None))


class obj:  # noqa: N801
    site_list = None
    sews = None
    tasker = None
    post_storage = None


class worker:  # noqa: N801
    sews = None
    scanner = None
    handler = None


check = Object(
    development=None,
)


config_parser = ConfigParser()


def load():
    global config_parser

    if "pytest" in sys.modules:
        config_parser.read("config.ci", encoding="utf-8")
    elif os.path.isfile("config"):
        config_parser.read("config", encoding="utf-8")
    else:
        config_parser.read("config.sample", encoding="utf-8")
    conf = config_parser['Config']

    config.read_key = conf.get('read_key', "IAkbitmze4B8KpacUfLqkw((")
    config.write_key = conf.get('write_key')
    config.write_token = conf.get('write_token')

    config.site = conf.get('site', "android.stackexchange.com")

    config.log_level = int(conf.get('log_level', 1))
    config.file_log_level = int(conf.get('file_log_level', 3))
    config.log_file = conf.get('log_file', "log.txt")

    config.db_file = conf.get('db_file', "androidoverflow.db")
    config.repo_slug = conf.get('repo_slug', "iBug/AndroidOverflow")
