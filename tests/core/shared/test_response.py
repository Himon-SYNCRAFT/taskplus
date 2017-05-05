import pytest
from unittest import mock
from taskplus.core.shared.response import ResponseSuccess, ResponseFailure
from taskplus.core.shared.request import RequestError


@pytest.fixture
def response_value():
    return {'key': ['value1', 'value2']}


@pytest.fixture
def response_type():
    return 'ResponseError'


@pytest.fixture
def response_msg():
    return 'This is a response error'


def test_response_success_is_true():
    assert bool(ResponseSuccess(response_value)) is True


def test_response_failure_is_false(response_type, response_msg):
    assert bool(ResponseFailure(response_type, response_msg)) is False


def test_response_success_contains_value(response_value):
    response = ResponseSuccess(response_value)
    assert response.value == response_value


def test_response_failure_has_type_and_message(response_type, response_msg):
    response = ResponseFailure(response_type, response_msg)
    assert response.type == response_type
    assert response.message == response_msg


def test_response_failure_contains_value(response_type, response_msg):
    response = ResponseFailure(response_type, response_msg)
    assert response.value == {
        'type': response_type, 'message': response_msg}


def test_response_failure_initialization_with_exception():
    error_message = 'Just an error message'
    response = ResponseFailure(response_type, Exception(error_message))

    assert bool(response) is False
    assert response.type == response_type
    assert response.message == 'Exception: {}'.format(error_message)


def test_response_failure_from_invalid_request():
    request = mock.Mock()
    request.errors = []
    request.is_valid.return_value = False

    response = ResponseFailure.build_from_invalid_request(request)
    assert bool(response) is False


def test_response_failure_from_invalid_request_with_errors():
    request = mock.Mock()
    request.errors = [
        RequestError('path', 'is mandatory'),
        RequestError('path', "can't be blank"),
    ]
    request.is_valid.return_value = False

    response = ResponseFailure.build_from_invalid_request(request)

    assert bool(response) is False
    assert response.type == ResponseFailure.PARAMETER_ERROR
    assert response.message == "path: is mandatory\npath: can't be blank"


def test_response_failure_build_resource_error():
    error_message = 'test message'
    response = ResponseFailure.build_resource_error(error_message)

    assert bool(response) is False
    assert response.type == ResponseFailure.RESOURCE_ERROR
    assert response.message == error_message


def test_response_failure_build_system_error():
    error_message = 'test message'
    response = ResponseFailure.build_system_error(error_message)

    assert bool(response) is False
    assert response.type == ResponseFailure.SYSTEM_ERROR
    assert response.message == error_message


def test_response_failure_build_paremeter_error():
    error_message = 'test message'
    response = ResponseFailure.build_parameter_error(error_message)

    assert bool(response) is False
    assert response.type == ResponseFailure.PARAMETER_ERROR
    assert response.message == error_message
