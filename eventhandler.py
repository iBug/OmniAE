import os

import core
from utils import log
import seapi


def on_new_post(j):
    log('debug', "New post ID: {}".format(j['id']))

    post = seapi.get_post(core.config.site, int(j['id']), "question")
    if not post:
        log('debug', "Fetched nothing for post {}".format(j['id']))
        return
    log('debug', "Fetched post: [{}] {}".format(post.id, post.title))
    core.worker.scanner.enqueue(post)
