from taskplus.apps.rest import models
from taskplus.apps.rest.database import db_session
from taskplus.core.domain import User, UserRole
from taskplus.core.shared.repository import Repository
from taskplus.core.shared.exceptions import NoResultFound


class UsersRepository(Repository):

    def __init__(self):
        self.user_model = models.User
        self.session = db_session

    def one(self, id):
        result = self.user_model.query.get(id)

        if not result:
            raise NoResultFound(id, User.__name__)

        role = UserRole(id=result.role.id, name=result.role.name)
        return User(name=result.name, role=role, id=result.id)

    def list(self, filters=None):
        if not filters:
            result = self.user_model.query.all()
        else:
            filters = self._parse_filters(filters)
            filters_expression = []

            for filter in filters:
                key = getattr(self.user_model, filter.key)
                filters_expression.append(
                    getattr(key, filter.operator)(filter.value))

            result = self.user_model.query.filter(*filters_expression).all()

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

        if not user_to_update:
            raise NoResultFound(user.id, User.__name__)

        user_to_update.name = user.name
        user_to_update.role_id = user.role.id

        self.session.add(user_to_update)
        self.session.commit()

        role = UserRole(id=user_to_update.role.id, name=user_to_update.role.name)
        return User(name=user_to_update.name, role=role, id=user_to_update.id)

    def delete(self, id):
        user = self.user_model.query.get(id)

        if not user:
            raise NoResultFound(id, User.__name__)

        role = UserRole(id=user.role.id, name=user.role.name)

        self.session.delete(user)
        self.session.commit()

        return User(name=user.name, role=role, id=user.id)
