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
            log('info', result.details)
            # core.obj.result_storage.add(result)
        if not result.active:
            log('info', "[{}] {}, score={}".format(
                post.id, post.title, round(result.score, 2)))
            return

        log('attention', "[{}] {} caught as {}, score={}".format(
            post.id, post.title, result.scanner.name, round(result.score, 2)))
        if result.scanner.name == "development question":
            if post.creation_date < datetime.now().timestamp() - 172800:  # 2 days
                log('attention', "Post too old ({}), ignored".format(
                    datetime.fromtimestamp(post.creation_date).isoformat()))
                return
            # log('attention', "Would add mod flag on <{}>".format(post.title))
            log('attention', "Adding close vote on [{}] {}".format(post.id, post.title))
            add_close_vote(post.site, post.id, 36662)
            # add_mod_flag(post.site, post.id,
            #              "question", "[Auto] Development question detected, score={}".format(
            #                  round(result.score, 2)))
        else:
            print("No handler implemented for {!r}".format(result.scanner))
