from unittest import mock

from taskplus.shared.request import InvalidRequest
from taskplus.shared.response import ResponseFailure
from taskplus.shared.use_case import UseCase


def test_use_case_cannot_process_valid_requests():
    request = mock.MagicMock()
    request.__bool__.return_value = True

    use_case = UseCase()
    response = use_case.execute(request)

    assert not response
    assert response.type == ResponseFailure.SYSTEM_ERROR
    msg = 'NotImplementedError: process_request() not implemented by ' +\
        'UseCase class'
    assert response.message == msg


def test_use_case_can_process_invalid_requests_and_returns_response_failure():
    request = InvalidRequest()
    parameter = 'parameter'
    message = 'message'
    request.add_error(parameter, message)

    use_case = UseCase()
    response = use_case.execute(request)

    assert not response
    assert response.type == ResponseFailure.PARAMETER_ERROR
    assert response.message == '{}: {}'.format(parameter, message)


def test_use_case_can_manage_generic_exception_process_request():
    use_case = UseCase()
    error_message = 'error'

    class TestException(Exception):
        pass

    use_case.process_request = mock.Mock()
    use_case.process_request.side_effect = TestException(error_message)
    response = use_case.execute(mock.Mock)

    assert not response
    assert response.type == ResponseFailure.SYSTEM_ERROR
    assert response.message == 'TestException: {}'.format(error_message)
