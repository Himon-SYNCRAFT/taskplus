from taskplus.apps.rest import models
from taskplus.apps.rest.database import db_session
from taskplus.core.domain import TaskStatus
from taskplus.core.shared.repository import Repository
from taskplus.core.shared.exceptions import (
    NoResultFound, NotUnique, CannotBeDeleted, DbError)
from sqlalchemy import exc


class TaskStatusesRepository(Repository):

    def __init__(self):
        self.status_model = models.TaskStatus
        self.session = db_session

    def one(self, id):
        status = self.status_model.query.get(id)

        if not status:
            raise NoResultFound(id, TaskStatus.__name__)

        return TaskStatus(id=status.id, name=status.name)

    def list(self, filters=None):
        if not filters:
            result = self.status_model.query.all()
        else:
            filters = self._parse_filters(filters)
            filters_expression = []

            for filter in filters:
                key = getattr(self.status_model, filter.key)
                filters_expression.append(
                    getattr(key, filter.operator)(filter.value))

            result = self.status_model.query.filter(*filters_expression).all()

        return [TaskStatus(id=status.id, name=status.name) for status in result]

    def update(self, status):
        status_to_update = self.status_model.query.get(status.id)

        if not status_to_update:
            raise NoResultFound(status.id, TaskStatus.__name__)

        try:
            status_to_update.name = status.name

            self.session.add(status_to_update)
            self.session.commit()

        except exc.IntegrityError as e:
            self.session.rollback()

            if 'unique' in str(e).lower():
                raise NotUnique('User already exist')
            raise

        except exc.SQLAlchemyError:
            self.session.rollback()
            raise DbError()

        return TaskStatus(id=status_to_update.id, name=status_to_update.name)

    def save(self, status):
        try:
            new_status = self.status_model(name=status.name)
            self.session.add(new_status)
            self.session.commit()

        except exc.IntegrityError as e:
            self.session.rollback()

            if 'unique' in str(e).lower():
                raise NotUnique('User already exist')

            raise

        except exc.SQLAlchemyError:
            self.session.rollback()
            raise DbError()

        return TaskStatus(id=new_status.id, name=new_status.name)

    def delete(self, id):
        status = self.status_model.query.get(id)

        if not status:
            raise NoResultFound(id, TaskStatus.__name__)

        try:
            self.session.delete(status)
            self.session.commit()

        except exc.IntegrityError as e:
            self.session.rollback()

            if 'foreign' in str(e).lower():
                raise CannotBeDeleted('Cannot delete user')
            raise

        except exc.SQLAlchemyError:
            self.session.rollback()
            raise DbError()

        return TaskStatus(id=id, name=status.name)
