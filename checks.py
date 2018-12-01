import regex

import core
from utils import log


development = core.check.development


@development.new("java code", 0.5)
def java_code(post):
    log('debug', "Running java code check")
    return 1.0, "Beta beta beta beta"
