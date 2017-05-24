from taskplus.apps.rest import models
from taskplus.apps.rest.database import db_session
from taskplus.core.domain import User, UserRole


class UsersRepository(object):

    def __init__(self):
        self.user_model = models.User
        self.session = db_session

    def one(self, user_id):
        result = self.user_model.query.get(user_id)

        if not result:
            return None

        role = UserRole(id=result.role.id, name=result.role.name)
        return User(name=result.name, role=role, id=result.id)

    def list(self, filters=None):
        if not filters:
            result = self.user_model.query.all()
            users = []

            for r in result:
                role = UserRole(id=r.role.id, name=r.role.name)
                user = User(name=r.name, role=role, id=r.id)

                users.append(user)

            return users

    def save(self, user):
        new_user = self.user_model(name=user.name, role_id=user.role.id)
        self.session.add(new_user)
        self.session.commit()

        role = UserRole(id=new_user.role.id, name=new_user.role.name)
        return User(name=new_user.name, role=role, id=new_user.id)

    def update(self, user):
        user_to_update = self.user_model.query.get(user.id)

        user_to_update.name = user.name
        user_to_update.role_id = user.role.id

        self.session.add(user_to_update)
        self.session.commit()

        role = UserRole(id=user_to_update.role.id, name=user_to_update.role.name)
        return User(name=user_to_update.name, role=role, id=user_to_update.id)
