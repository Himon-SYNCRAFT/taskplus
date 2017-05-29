from taskplus.apps.rest import models
from taskplus.apps.rest.database import db_session
from taskplus.core.domain import UserRole
from taskplus.core.shared.repository import Repository


class UserRolesRepository(Repository):

    def __init__(self):
        self.role_model = models.UserRole
        self.session = db_session

    def list(self, filters=None):
        if not filters:
            result = self.role_model.query.all()
        else:
            filters = self._parse_filters(filters)
            filters_expression = []

            for filter in filters:
                key = getattr(self.role_model, filter.key)
                filters_expression.append(
                    getattr(key, filter.operator)(filter.value))

            result = self.role_model.query.filter(*filters_expression).all()
        return [UserRole(id=role.id, name=role.name) for role in result]

    def one(self, id):
        result = self.role_model.query.filter_by(id=id).one()
        return UserRole(id=result.id, name=result.id)

    def update(self, role):
        role_to_update = self.role_model.query.filter_by(id=role.id).one()
        role_to_update.name = role.name

        self.session.add(role_to_update)
        self.session.commit()

        return UserRole(id=role_to_update.id, name=role_to_update.name)

    def save(self, role):
        new_role = self.role_model(name=role.name)
        self.session.add(new_role)
        self.session.commit()

        return UserRole(id=new_role.id, name=new_role.name)

    def delete(self, id):
        role_to_delete = self.role_model.query.filter_by(id=id).one()
        role = UserRole(id=role_to_delete.id, name=role_to_delete.name)

        self.session.delete(role_to_delete)
        self.session.commit()

        return role
