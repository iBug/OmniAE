from gitmanager import *


def test_is_same_commit():
    assert is_same_commit("HEAD", "HEAD")
    assert not is_same_commit("HEAD", "HEAD~")
