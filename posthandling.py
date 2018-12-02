import core
from utils import log
from seapi import add_mod_flag


class PostHandler:
    def __init__(self):
        pass

    def handle(self, result):
        if not result.active:
            log('info', "Post {} inactive result, score={:.3g}".format(result.post.title, result.score))
            return

        post = result.post
        if result.scanner.name == "development question":
            log('debug', "Adding mod flag on <{}>".format(post.title))
            add_mod_flag(post.site, post.id, "question", "[Auto] Development question detected")
        else:
            print(result.scanner)
        log('info', "[{}] {} caught for {}, score={:.3g}".format(
            result.post.id, result.post.title, result.scanner.name, result.score))
