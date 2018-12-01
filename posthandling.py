from utils import log
from seapi import add_mod_flag


class PostHandler:
    def __init__(self):
        pass

    def handle(self, result):
        if not result.active:
            log('info', "Post {} inactive result, score={}".format(result.post.title, result.score))
            return

        post = result.post
        if result.scanner is core.check.development:
            add_mod_flag(post.site, post.id, "question", "[Auto] Development question detected")
        log('info', "Post {} caught for {}, score={}".format(
            result.post.title, result.scanner.name, result.score))
