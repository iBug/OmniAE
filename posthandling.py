from utils import log


class PostHandler:
    def __init__(self):
        pass

    def handle(self, result):
        if not result.active:
            log('info', "Post {} inactive result, score={}".format(result.post.title, result.score))
            return

        log('info', "Post {} caught for {} with score {}".format(
            result.post.title, result.scanner.name, result.score))
