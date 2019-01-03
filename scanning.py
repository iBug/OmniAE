import core


class PostCheck:
    """
    A single check against posts
    """
    def __init__(self, func, reason, threshold=0.0, multiplier=1.0):
        self.func = func
        self.reason = reason
        self.threshold = threshold
        self.multiplier = multiplier

    def run(self, post):
        score, detail = self.func(post)
        return score * self.multiplier, detail

    def __call__(self, post):
        return self.run(post)


class PostScanResult:
    def __init__(self, post, scanner, score, reasons, details):
        self.post = post
        self.scanner = scanner
        self.score = score
        self.reasons = reasons
        self.details = details

    @property
    def active(self):
        return self.score >= self.scanner.threshold


class PostScanner:
    """
    A collection of checks that together determines whether a post is of a certain kind
    """

    def __init__(self, name="", threshold=1.0):
        self.name = name
        self.checks = []
        self.threshold = threshold

    def new(self, reason, threshold=0.0, multiplier=1.0):
        def decorator(f):
            check = PostCheck(f, reason, threshold, multiplier)
            self.checks.append(check)
            return f
        return decorator

    def check_post(self, post):
        score = 0.0
        reasons = []
        details = []
        for check in self.checks:
            check_score, check_details = check.run(post)
            score += check_score
            if check_score >= check.threshold:
                reasons.append(check.reason)
                details.append(check_details)
        return PostScanResult(post, self, score, reasons, "\n".join(details))
