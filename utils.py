import sys
import os
import datetime
import traceback

from termcolor import colored

import core


_LOG_CONFIG = {
    'debug': (0, 'gray'),
    'info': (1, 'cyan'),
    'warning': (2, 'yellow'),
    'error': (3, 'red'),
}


def log(log_level, *args):
    level, color = _LOG_CONFIG[log_level]
    if level < core.config.log_level:
        return

    time_s = datetime.now().isoformat()[11:23]
    s = "{} {}".format(colored("[{}]".format(time_s), color, attrs=['bold']),
                       "\n             ".join([str(x) for x in args]))
    print(s, file=sys.stderr)
    if level == 3:
        traceback.print_stack()

    log_file(log_level, *args)


def log_file(log_level, *args):
    level = _LOG_CONFIG[log_level][0]
    if level < core.config.file_log_level:
        return

    time_s = datetime.now().isoformat()[11:23]
    log_s = "\n             ".join([str(x) for x in args])
    with open(core.config.log_file) as f:
        print("[{}] {}".format(time_s, log_s), file=f)
