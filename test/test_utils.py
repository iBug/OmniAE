import utils
from utils import *

from unittest.mock import patch


@patch("utils.log")
def test_log_exception(log):
    exc_obj = ValueError("Some random text")
    assert log_exception(exc_obj) is None
    assert log.call_count == 1
    assert log.call_args_list[-1][0] == ('error', "ValueError: Some random text")
    assert log.call_args_list[-1][1] == dict()

    try:
        raise TypeError("Another exception")
    except Exception:
        assert log_exception() is None
        assert log.call_count == 2
        assert log.call_args_list[-1][0] == ('error', "TypeError: Another exception")
        assert log.call_args_list[-1][1] == dict()
