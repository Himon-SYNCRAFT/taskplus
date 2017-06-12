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

        return self._to_domain_model(result)

    def list(self, filters=None):
        if not filters:
            result = self.user_model.query.all()
        else:
            print('t')
            filters = self._parse_filters(filters)
            filters_expression = []

            for filter in filters:
                key = getattr(self.user_model, filter.key)
                filters_expression.append(
                    getattr(key, filter.operator)(filter.value))

            result = self.user_model.query.filter(*filters_expression).all()

        users = [self._to_domain_model(user) for user in result]

        return users

    def save(self, user, password):
        roles = models.UserRole.query.filter(
            models.UserRole.id.in_([role.id for role in user.roles])).all()

        new_user = self.user_model(name=user.name, roles=roles, password=password)
        self.session.add(new_user)
        self.session.commit()

        return self._to_domain_model(new_user)

    def update(self, user):
        user_to_update = self.user_model.query.get(user.id)

        if not user_to_update:
            raise NoResultFound(user.id, User.__name__)

        roles = models.UserRole.query.filter(
            models.UserRole.id.in_([role.id for role in user.roles])).all()

        user_to_update.name = user.name
        user_to_update.roles = roles

        self.session.add(user_to_update)
        self.session.commit()

        return self._to_domain_model(user_to_update)

    def delete(self, id):
        user = self.user_model.query.get(id)

        if not user:
            raise NoResultFound(id, User.__name__)

        rv = self._to_domain_model(user)

        self.session.delete(user)
        self.session.commit()

        return rv

    def _to_domain_model(self, data):
        return User(
            id=data.id,
            name=data.name,
            roles=[UserRole(id=role.id, name=role.name)
                   for role in data.roles]
        )

    def check_password(self, user, password):
        result = self.user_model.query.get(user.id)

        if not result:
            raise NoResultFound(id, User.__name__)

        return result.check_password(password)
