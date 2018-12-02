# LOL. Hope you're not fooled by the name of this file


import os
from configparser import ConfigParser


# Note: All classes here have N801 (CapWords naming convention) disabled.
# They're intended to be singletons


class config:  # noqa: N801
    read_key = None
    write_key = None
    write_token = None

    site = None
    site_id = None

    log_level = None
    file_log_level = None
    log_file = "log.txt"

    commit_info = None


class obj:  # noqa: N801
    site_list = None
    sews = None
    tasker = None


class worker:  # noqa: N801
    sews = None
    scanner = None
    handler = None


class check:  # noqa: N801
    development = None


config_parser = ConfigParser()


def load():
    global config_parser

    if os.path.isfile("config"):
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
