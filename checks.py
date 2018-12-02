import math
import regex

import core
from utils import log
from scanning import PostScanner


development = core.check.development = PostScanner("development question", 1.99)


@development.new("bracket count", 1.4)
def bracket_count(post):
    score = 0.0
    body = post.title + "\n\n" + post.raw_body

    n_brackets = body.count("{") + body.count("}")
    if n_brackets >= 3:
        score += math.sqrt(n_brackets - 3)

    return score, "Post has {} brackets".format(n_brackets)


@development.new("java keyword", 1.0)
def java_keyword(post):
    score = 0.0
    body = post.title + "\n\n" + post.raw_body

    n = body.count("public")
    if n >= 5:
        score += (n - 5) / 10
    n = body.count("class")
    if n >= 2:
        score += (n - 2) / 8
    n = body.count("@Override")
    score += n / 2
    return score, "Post has Java keyword"


@development.new("android code", 1.5)
def android_code(post):
    score = 0.0
    body = post.title + "\n\n" + post.raw_body

    match = regex.compile(
        r"\b[A-Za-z]{2,}(?:Activity|Fragment|View|Text|Exception|Manager|Method)\b"
    ).findall(body)
    score += len(match)

    match = regex.compile(r"\b[A-Z]+(?:_[A-Z]+)+\b").findall(body)
    score += len(match)

    match = regex.compile(
        r"\b(?:MainActivity|onCreate|layout|private class|public class|Bundle)\b"
    ).findall(body)
    score += len(match)

    return score, "Post has Android code"
