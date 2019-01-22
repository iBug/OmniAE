import github


def test_ci_status():
    assert github.ci_status() is True
