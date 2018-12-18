import sqlite3
import threading


class LocalStorage:
    def __init__(self, filename):
        self.dbs = {}
        self.filename = filename

    def open(self):
        thread_id = threading.get_ident()
        if thread_id not in self.dbs:
            self.dbs[thread_id] = sqlite3.connect(self.filename)
        return self.dbs[thread_id]
