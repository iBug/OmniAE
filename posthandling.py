from datetime import datetime

import core
from utils import log
from seapi import add_mod_flag


class PostHandler:
    def __init__(self):
        pass

    def handle(self, result):
        if not result.active:
            log('info', "[{}] {}, score={:.3g}".format(
                result.post.id, result.post.title, result.score))
            return

        post = result.post
        if result.scanner.name == "development question":
            if post.creation_date < datetime.now().timestamp() - 172800:  # 2 days
                log('attention', "Post too old ({}), ignored, score={}".format(
                    datetime.fromtimestamp(post.creation_date).isoformat(),
                    result.score))
                return
            log('attention', "Adding mod flag on <{}>".format(post.title))
            add_mod_flag(post.site, post.id,
                         "question", "[Auto] Development question detected, score={:.3g}".format(
                             result.score))
        else:
            print(result.scanner)
        log('attention', "[{}] {} caught for {}, score={:.3g}".format(
            result.post.id, result.post.title, result.scanner.name, result.score))
