import math
import regex
re = regex.compile

import core
from utils import log
from scanning import PostScanner


development = core.check.development = PostScanner("development question", 3.99)


@development.new("bracket count", 1.4)
def bracket_count(post):
    score = 0.0
    body = post.title + "\n\n" + post.raw_body

    n_brackets = len(re(r"[{}](?=[ \t]*(?:\n|$))").findall(body)) + len(regex.compile(r"(?<=\w)\(\)(?=[\s);])").findall(body))
    if n_brackets >= 3:
        score = math.sqrt(n_brackets - 3)

    return score, "Post has {} brackets".format(n_brackets)


@development.new("java code", 1.0)
def java_keyword(post):
    score = 0.0
    body = post.title + "\n\n" + post.raw_body
    s = []

    n = body.count("public")
    if n >= 5:
        score += (n - 5) / 10
    n = re(r"\b(?:class|void|int|boolean)\b").findall(body)
    if len(n) >= 2:
        score += (len(n) - 2) / 2
        s.append("Keywords: " + ", ".join([repr(x) for x in n]))
    n = body.count("@Override")
    score += n

    m = re(r"(public|protected|private)\s+(class|void|int|boolean)", flags=2).findall(body)
    score += len(m) * 1.5
    if m:
        s.append("Keywords: " + ", ".join([repr(x) for x in m]))

    m = re(r"new\s+[A-Z]\w+\(").findall(body)  # new Asdfgh(
    score += len(m) * 1.5
    if m:
        s.append("Keywords: " + ", ".join([repr(x) for x in m]))

    m = re(r"(?<!\s)\.\w+\((?!\w+\.java:\d+\))").findall(body)  # a.b(
    score += len(m) * 1.5
    if m:
        s.append("Keywords: " + ", ".join([repr(x) for x in m]))
    return score, "Java code:\n" + "\n".join(s)


@development.new("android code", 1.5)
def android_code(post):
    score = 0.0
    body = post.title + "\n\n" + post.raw_body
    s = []

    match = re(
        r"(?s)(?<!\.)[A-Za-z]{2,}(?:"
        r"Activity|Fragment|(?<!(?i:web\s*))View|Text|Exception|Manager|Method|Interface|Listener|Request|Layout|Drawable"
        r")\b"
    ).findall(body)
    score += len(match)
    if match:
        s.append("Keywords: " + ", ".join([repr(x) for x in match]))

    keywords = "|".join([
        r"(?i:Text|Grid|List|Recycler)\s*View"
    ])
    match = re(r"(?i)\b({})\b".format(keywords)).findall(body)
    score += len(match)
    if match:
        s.append("Keywords: " + ", ".join([repr(x) for x in match]))

    match = re(r"\b[A-Z]+(?:_[A-Z]+)+\b").findall(body)
    score += len(match) * 0
    if match:
        s.append("Keywords: " + ", ".join([repr(x) for x in match]))

    match = re(r'\bandroid:\w+="').findall(body)
    score += len(match) * 1
    if match:
        s.append("Keywords: " + ", ".join([repr(x) for x in match]))

    match = re(
        r"\b(?:MainActivity|AppCompatActivity|onCreate)\b"
    ).findall(body)
    score += len(match) * 2.0
    if match:
        s.append("Keywords: " + ", ".join([repr(x) for x in match]))

    match = re(r"(?i)android\W*studio").findall(body)
    score += bool(match)
    if match:
        s.append("Keywords: " + ", ".join([repr(x) for x in match]))

    return score, "Android code:\n" + "\n".join(s)


@development.new("coding intention", 1.0)
def coding_intention(post):
    score = 0.0
    body = post.title + "\n\n" + post.raw_body
    s = []

    match = re(r"(?i)\b(?:build|wr[io]t|develop|cre?at|ma[dk]|compil)e?d?(?:ing)?\b.{,20}\b(?:app(?:lication)?|intent|code|program\w*|driver)s?\b").findall(body)
    score += len(match) * 2.0
    s.append("Keywords: " + ", ".join([repr(x) for x in match]))

    match = re(r"(?i)\bmy\b.{,20}\bapp(?:lication)?s?\b").findall(body)
    if match:
        score += 0.5
        s.append("Keywords: " + ", ".join([repr(x) for x in match]))

    return score, "Coding intention:\n" + "\n".join(s)
