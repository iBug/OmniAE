from scanning import *


def test_postscanresult():
    test_scanner = PostScanner()
    test = PostScanResult(None, test_scanner, 2.0, [], "")
    assert test.active
    test.score = 0.0
    assert not test.active
