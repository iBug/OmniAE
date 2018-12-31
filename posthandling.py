from datetime import datetime

import core
from utils import log
from seapi import add_mod_flag


class PostHandler:
    def __init__(self):
        pass

    def handle(self, result):
        post = result.post
        if result.score >= 0.01:
            core.obj.post_storage.add(post)
        if not result.active:
            log('info', "[{}] {}, score={:.3g}".format(
                post.id, post.title, result.score))
            return

        log('attention', "[{}] {} caught as {}, score={:.3g}".format(
            post.id, post.title, result.scanner.name, result.score))
        if result.scanner.name == "development question":
            if post.creation_date < datetime.now().timestamp() - 172800:  # 2 days
                log('attention', "Post too old ({}), ignored, score={}".format(
                    datetime.fromtimestamp(post.creation_date).isoformat(),
                    result.score))
                return
            log('attention', "Adding mod flag on <{}>".format(post.title))
            add_mod_flag(post.site, post.id,
                         "question", "[Auto] Development question detected, score={:.2g}".format(
                             result.score))
        else:
            print("No handler implemented for {!r}".format(result.scanner))
