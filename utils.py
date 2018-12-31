import sys
import os
import datetime
import traceback

import requests
from termcolor import colored

import core


_LOG_CONFIG = {
    'debug': (0, 'grey'),
    'info': (1, 'cyan'),
    'warning': (2, 'yellow'),
    'error': (3, 'red'),
    'attention': (1, 'green'),
    'status': (1, 'magenta'),
    '???': (1, 'blue'),
}


def log(log_level, *args):
    level, color = _LOG_CONFIG[log_level]
    if level < core.config.log_level:
        return

    time_s = datetime.datetime.now().isoformat()[11:23]
    s = "{} {}".format(colored("[{}]".format(time_s), color, attrs=['bold']),
                       "\n             ".join([str(x) for x in args]))
    print(s, file=sys.stderr)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    if exc_obj is not None:
        print("".join(traceback.format_tb(exc_tb)))

    log_file(log_level, *args)


def log_file(log_level, *args):
    level = _LOG_CONFIG[log_level][0]
    if level < core.config.file_log_level:
        return

    time_s = datetime.datetime.now().isoformat()[11:23]
    log_s = "\n             ".join([str(x) for x in args])
    with open(core.config.log_file, "a") as f:
        print("[{}] {}".format(time_s, log_s), file=f)


def log_exception(exc_obj=None, exc_tb=None):
    if exc_obj is None:
        exc_obj = sys.exc_info()[1]
    if exc_obj is None:
        return  # No exception, huh?
    exc_s = "{}: {}".format(type(exc_obj).__name__, str(exc_obj))
    log('error', exc_s)
