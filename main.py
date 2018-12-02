#!/usr/bin/env python3

import sys
from excepthook import uncaught_exception, install_thread_excepthook
sys.excepthook = uncaught_exception
install_thread_excepthook()
# Exception hook installed, can proceed now

import os
from threading import Thread

import core
from utils import log
from seapi import get_site_id
from tasking import Tasker
from gitmanager import check_for_updates
import workers


def register_tasks():
    core.tasker = Tasker()
    core.tasker.periodic(check_for_updates, interval=60)


def main():
    core.load()

    register_tasks()

    site_id = get_site_id(core.config.site)
    log('debug', "Fetched site ID {} from {}".format(site_id, core.config.site))
    core.config.site_id = site_id

    core.worker.sews.start()
    core.worker.scanner.start()
    core.worker.handler.start()


if __name__ == "__main__":
    main()
