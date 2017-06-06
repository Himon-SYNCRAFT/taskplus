from flask_login import LoginManager
from flask import jsonify

from taskplus.core.actions import ListUsersAction, ListUsersRequest
from taskplus.apps.rest.repositories import UsersRepository


login_manager = LoginManager()


@login_manager.user_loader
def user_loader(name):
    repository = UsersRepository()
    request = ListUsersRequest(filters=dict(name=name))
    action = ListUsersAction(repo=repository)
    response = action.execute(request)

    if not response or not response.value:
        return None

    user = response.value[0]
    user.is_active = True
    user.is_authenticated = True
    user.is_anonymous = False
    user.get_id = lambda _: user.name

    return user


@login_manager.request_loader
def request_loader(request):
    name = request.form.get('name')

    repository = UsersRepository()
    request = ListUsersRequest(filters=dict(name=name))
    action = ListUsersAction(repo=repository)
    response = action.execute(request)

    if not response or not response.value:
        return None

    user = response.value[0]
    user.is_authenticated = repository.check_password(
        user, request.form['password'])
    user.is_active = True
    user.is_anonymous = False
    user.get_id = lambda _: user.name

    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    message = 'Unauthorized'
    return jsonify(dict(message=message)), 401
