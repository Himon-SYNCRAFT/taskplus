from taskplus.shared.response import ResponseSuccess


def test_response_success_is_true():
    assert bool(ResponseSuccess()) is True
