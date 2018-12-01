#!/usr/bin/env python3

import os
import sys
from threading import Thread

import core
from sews import StackExchangeWebSocket
import eventhandlers
from utils import log, get_site_id


def main():
    core.load()
    
    site_id = get_site_id(core.config.site)
    log('debug', "Fetched site ID {} from {}".format(site_id, core.config.site))

    sews = core.obj.sews = StackExchangeWebSocket()
    sews.open()
    sews.register("{}-home-active".format(site_id), eventhandlers.on_new_post)
    core.thread.sews = Thread(name="sews", target=sews.event_loop)
    core.thread.sews.start()


if __name__ == "__main__":
    main()
