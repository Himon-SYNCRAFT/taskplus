from unittest import mock

from taskplus.core.shared.request import RequestError
from taskplus.core.shared.response import ResponseFailure
from taskplus.core.shared.action import Action


def test_action_cannot_process_valid_requests():
    request = mock.MagicMock()
    request.__bool__.return_value = True

    action = Action()
    response = action.execute(request)

    assert not response
    assert response.type == ResponseFailure.SYSTEM_ERROR
    msg = 'NotImplementedError: process_request() not implemented by ' +\
        'Action class'
    assert response.message == msg


def test_action_can_process_invalid_requests_and_returns_response_failure():
    parameter = 'parameter'
    message = 'message'

    request = mock.Mock()
    request.is_valid.return_value = False
    request.errors = [RequestError(parameter, message)]

    action = Action()
    response = action.execute(request)

    assert not response
    assert response.type == ResponseFailure.PARAMETER_ERROR
    assert response.message == '{}: {}'.format(parameter, message)


def test_action_can_manage_generic_exception_process_request():
    action = Action()
    error_message = 'error'

    class TestException(Exception):
        pass

    request = mock.Mock()
    request.is_valid.return_value = True

    action.process_request = mock.Mock()
    action.process_request.side_effect = TestException(error_message)
    response = action.execute(request)

    assert not response
    assert response.type == ResponseFailure.SYSTEM_ERROR
    assert response.message == 'TestException: {}'.format(error_message)
