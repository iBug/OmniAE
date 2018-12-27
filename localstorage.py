import sqlite3
import threading


class LocalStorage:
    def __init__(self, filename: str):
        self.dbs = {}
        self.filename = filename

    def open(self):
        thread_id = threading.get_ident()
        if thread_id not in self.dbs:
            self.dbs[thread_id] = sqlite3.connect(self.filename)
        return self.dbs[thread_id]

    def __call__(self, query: str, params=(), **kwargs):
        return self.execute(query, params, **kwargs)

    def execute(self, query: str, params=(), **kwargs):
        thread_id = threading.get_ident()
        try:
            db = self.dbs[thread_id]
        except KeyError:
            raise
        return db.execute(query, tuple(params), **kwargs)

    def table_exists(self, table="sqlite_master"):
        return bool(self.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [table]))


class PostStorage(LocalStorage):
    def __init__(self, filename):
        self.ls = LocalStorage(filename)

    def open(self):
        self.ls.open()

    def initialize(self):
        pass

    def add(self, post):
        pass
