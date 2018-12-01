from threading import Thread
from queue import Queue

import core
import eventhandler
from sews import StackExchangeWebSocket


class Worker:
    def __init__(self):
        pass

    def start(self):
        pass


class SEWSWorker(Worker):
    def __init__(self):
        self.ws = StackExchangeWebSocket()
        self.thread = Thread(name="se websocket", target=self.ws.event_loop)

    def start(self):
        self.ws.open()
        self.ws.register("{}-home-active".format(core.config.site_id), eventhandler.on_new_post)
        self.thread.start()


class PostScannerWorker(Worker):
    def __init__(self):
        self.q = Queue

    def start(self):
        pass


class PostHandlerWorker(Worker):
    def __init__(self):
        pass

    def start(self):
        pass


core.worker.sews = SEWSWorker()
core.worker.scanner = PostScannerWorker()
core.worker.handler = PostHandlerWorker()
