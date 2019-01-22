import core


def test_core():
    core.load()
    assert core.config.write_key == "(((write_key)))"
    assert core.config.write_token == "(((write_token)))"
