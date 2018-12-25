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

    def __call__(self, query, params=(), **kwargs):
        return self.execute(query, params, **kwargs)

    def execute(self, query, params=(), **kwargs):
        thread_id = threading.get_ident()
        try:
            db = self.dbs[thread_id]
        except KeyError:
            raise
        return db.execute(query, tuple(params), **kwargs)


class PostStorage(LocalStorage):
    def __init__(self):
        raise NotImplementedError
