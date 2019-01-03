import sqlite3
import threading


class LocalStorage:
    def __init__(self, filename: str, auto_open=True):
        self.dbs = {}
        self.filename = filename
        self.auto_open = auto_open

    def open(self):
        thread_id = threading.get_ident()
        if thread_id not in self.dbs:
            self.dbs[thread_id] = sqlite3.connect(self.filename)
        return self.dbs[thread_id]

    def get_db(self, thread_id=None):
        thread_id = thread_id or threading.get_ident()
        if self.auto_open:
            return self.open()
        elif thread_id in self.dbs:
            return self.dbs[thread_id]
        else:
            return None

    def __call__(self, query: str, params=(), **kwargs):
        r = self.execute(query, params, **kwargs)
        self.commit()
        return r

    def execute(self, query: str, params=(), **kwargs):
        return self.get_db().execute(query, tuple(params), **kwargs)

    def commit(self):
        self.get_db().commit()

    def create_table(self, table, schema):
        if self.table_exists(table):
            return False
        r = self.execute("CREATE TABLE {} ({})".format(table, ", ".join(schema)))
        self.commit()
        return r

    def table_exists(self, table="sqlite_master"):
        return bool(self.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", [table]).fetchall())


class PostStorage(LocalStorage):
    table = "posts"

    def __init__(self, filename):
        self.ls = LocalStorage(filename)
        self.initialize()

    def open(self):
        self.ls.open()

    def initialize(self):
        self.ls.create_table(self.table, ["id INTEGER", "url TEXT PRIMARY KEY", "type TEXT", "site TEXT", "owner_url TEXT", "owner_name TEXT", "owner_rep INTEGER", "title TEXT", "body TEXT", "raw_body TEXT", "score INTEGER", "upvote INTEGER", "downvote INTEGER", "question_id INTEGER", "creation_date INTEGER", "last_edit_date INTEGER"])

    def add(self, post):
        return self.ls("INSERT INTO {} VALUES ({})".format(self.table, ", ".join("?" * 16)), params=post.to_list())
