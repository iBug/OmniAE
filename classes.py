class Post:
    __getitem__ = getattr
    __setitem__ = setattr

    def __init__(self):
        self.id = None
        self.url = None
        self.type = None
        self.site = None
        self.owner_url = None
        self.owner_name = None
        self.owner_rep = None
        self.title = None
        self.body = None
        self.raw_body = None
        self.score = None
        self.upvote = None
        self.downvote = None
        self.question_id = None
        self.creation_date = None
        self.last_edit_date = None
