from unittest import mock

from taskplus.core.actions import DeleteUserAction, DeleteUserRequest
from taskplus.core.shared.response import ResponseFailure


def test_delete_user_action():
    user_id = 1
    repo = mock.Mock()
    repo.delete.return_value = user_id
    request = DeleteUserRequest(id=user_id)
    action = DeleteUserAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is True
    assert response.value == repo.delete.return_value
    repo.delete.assert_called_once()


def test_delete_user_action_handles_bad_request():
    user_id = None
    repo = mock.Mock()
    repo.delete.return_value = user_id
    request = DeleteUserRequest(id=user_id)
    action = DeleteUserAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is False
    assert not repo.delete.called
    assert response.value == {
        'type': ResponseFailure.PARAMETER_ERROR,
        'message': 'id: is required'
    }


def test_delete_user_action_handles_excetion():
    error_message = 'Error!!!'
    user_id = 1
    repo = mock.Mock()
    repo.delete.side_effect = Exception(error_message)
    request = DeleteUserRequest(id=user_id)
    action = DeleteUserAction(repo=repo)
    response = action.execute(request)

    assert bool(response) is False
    assert repo.delete.called
    assert response.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: {}'.format(error_message)
    }
