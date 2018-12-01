from threading import Thread
from queue import Queue

import core
import eventhandler
from sews import StackExchangeWebSocket
from scanning import PostScanner
from posthandling import PostHandler


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
        self.q = Queue()
        self.thread = Thread(name="post scanner", target=self.event_loop)
        self.scanner = core.check.development

    def start(self):
        self.thread.start()

    def event_loop(self):
        while True:
            post = self.q.get()
            result = self.scanner.check_post(post)
            core.worker.handler.enqueue(result)

    def enqueue(self, post):
        self.q.put(post)


class PostHandlerWorker(Worker):
    def __init__(self):
        self.q = Queue()
        self.thread = Thread(name="post handler", target=self.event_loop)
        self.handler = PostHandler()

    def start(self):
        self.thread.start()

    def enqueue(self, result):
        self.q.put(result)

    def event_loop(self):
        while True:
            result = self.q.get()
            self.handler.handle(result)


core.worker.sews = SEWSWorker()
core.worker.scanner = PostScannerWorker()
core.worker.handler = PostHandlerWorker()
