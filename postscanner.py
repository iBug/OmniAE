import regex

import core


class PostCheckResult:
    def __init__(self, check=None, score=None, reasons=None, details=None):
        self.check = check
        self.score = score or 0.0
        self.reasons = reasons or []
        self.details = details or ""


class PostCheck:
    """
    A single check against posts
    """
    def __init__(self, func, reason):
        self.func = func
        self.reason = reason

    def run(self, post):
        return self.func(post)


def create_check(reason):
    """
    A decorator that turns a function into a PostCheck object
    """
    def decorator(f):
        return PostCheck(f, reason=reason)


class PostChecker:
    """
    A collection of checks that together determines whether a post is of a certain kind
    """

    def __init__(self, checks, name=""):
        self.name = name
        self.checks = checks

    def check_post(self, post):
        for check in checks:
            check_score, check_details = check(post)
