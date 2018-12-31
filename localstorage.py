import sqlite3
import threading


class LocalStorage:
    def __init__(self, filename: str, auto_open: bool=True):
        self.dbs = {}
        self.filename = filename
        self.auto_open = auto_open

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
            if self.auto_open:
                db = self.open()
            else:
                db = self.dbs[thread_id]
        except KeyError:
            raise
        return db.execute(query, tuple(params), **kwargs)

    def create_table(self, table, schema):
        if self.table_exists(table):
            return False
        return self.execute("CREATE TABLE {} ({})".format(table, ", ".join(schema)))

    def table_exists(self, table="sqlite_master"):
        return bool(self.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", [table]))


class PostStorage(LocalStorage):
    table = "posts"

    def __init__(self, filename):
        self.ls = LocalStorage(filename)
        self.open()
        self.initialize()

    def open(self):
        self.ls.open()

    def initialize(self):
        self.ls.create_table(self.table, ["id INTEGER", "url TEXT PRIMARY KEY", "type TEXT", "site TEXT", "owner_url TEXT", "owner_name TEXT", "owner_rep INTEGER", "title TEXT", "body TEXT", "raw_body TEXT", "score INTEGER", "upvote INTEGER", "downvote INTEGER", "question_id INTEGER", "creation_date INTEGER", "last_edit_date INTEGER"])

    def add(self, post):
        return self.ls.execute("INSERT INTO {} VALUES ({})".format(self.table, ", ".join("?" * 16)), params=post.to_list())
