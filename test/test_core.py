import core


def test_core():
    assert core.config.write_key is None
    assert core.config.write_token is None
