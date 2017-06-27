from taskplus.apps.rest import models
from taskplus.apps.rest.database import db_session
from taskplus.core.domain import UserRole
from taskplus.core.shared.repository import Repository
from taskplus.core.shared.exceptions import (
    NoResultFound, NotUnique, DbError, CannotBeDeleted)
from sqlalchemy import exc


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
        result = self.role_model.query.get(id)

        if not result:
            raise NoResultFound(id, UserRole.__name__)

        return UserRole(id=result.id, name=result.name)

    def update(self, role):
        role_to_update = self.role_model.query.get(role.id)

        if not role_to_update:
            raise NoResultFound(role.id, UserRole.__name__)

        try:
            role_to_update.name = role.name
            self.session.add(role_to_update)
            self.session.commit()

        except exc.IntegrityError as e:
            self.session.rollback()

            if 'unique' in str(e).lower():
                raise NotUnique('User already exist')
            raise

        except exc.SQLAlchemyError:
            self.session.rollback()
            raise DbError()

        return UserRole(id=role_to_update.id, name=role_to_update.name)

    def save(self, role):
        try:
            new_role = self.role_model(name=role.name)
            self.session.add(new_role)
            self.session.commit()

        except exc.IntegrityError as e:
            self.session.rollback()

            if 'unique' in str(e).lower():
                raise NotUnique('User already exist')

            raise

        except exc.SQLAlchemyError:
            self.session.rollback()
            raise DbError()

        return UserRole(id=new_role.id, name=new_role.name)

    def delete(self, id):
        role_to_delete = self.role_model.query.get(id)

        if not role_to_delete:
            raise NoResultFound(id, UserRole.__name__)

        try:
            role = UserRole(id=role_to_delete.id, name=role_to_delete.name)
            self.session.delete(role_to_delete)
            self.session.commit()

        except exc.IntegrityError as e:
            self.session.rollback()

            if 'foreign' in str(e).lower():
                raise CannotBeDeleted('Cannot delete user')
            raise

        except exc.SQLAlchemyError:
            self.session.rollback()
            raise DbError()

        return role
