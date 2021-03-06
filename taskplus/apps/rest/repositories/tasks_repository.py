from taskplus.apps.rest import models
from taskplus.apps.rest.database import db_session
from taskplus.core.shared.repository import Repository
from taskplus.core.domain import Task, User, TaskStatus, UserRole
from taskplus.core.shared.exceptions import (
    NoResultFound, NotUnique, CannotBeDeleted, DbError)
from sqlalchemy import exc


class TasksRepository(Repository):

    def __init__(self):
        self.task_model = models.Task
        self.session = db_session

    def one(self, id):
        result = self.task_model.query.get(id)

        if not result:
            raise NoResultFound(id, Task.__name__)

        return self._to_domain_model(result)

    def list(self, filters=None):
        if not filters:
            result = self.task_model.query.all()
        else:
            filters = self._parse_filters(filters)
            result = self.task_model.query.filter(*filters).all()

        return [self._to_domain_model(task) for task in result]

    def update(self, task):
        task_to_update = self.task_model.query.get(task.id)

        if not task_to_update:
            raise NoResultFound(task.id, Task.__name__)

        doer_id = None

        if task.doer:
            doer_id = task.doer.id
            doer = models.User.query.get(doer_id)
            if not doer:
                raise NoResultFound(doer_id, 'User')

        creator = models.User.query.get(task.creator.id)

        if not creator:
            raise NoResultFound(task.creator.id, 'User')

        if not models.TaskStatus.query.get(task.status.id):
            raise NoResultFound(task.status.id, 'TaskStatus')

        try:
            task_to_update.status_id = task.status.id
            task_to_update.creator_id = task.creator.id

            task_to_update.doer_id = doer_id

            task_to_update.content = task.content
            task_to_update.name = task.name

            self.session.add(task_to_update)
            self.session.commit()

        except exc.IntegrityError as e:
            self.session.rollback()

            if 'unique' in str(e).lower():
                raise NotUnique('Task already exist')
            raise

        except exc.SQLAlchemyError:
            self.session.rollback()
            raise DbError()

        return self._to_domain_model(task_to_update)

    def save(self, task):
        doer_id = None

        if task.doer:
            doer_id = task.doer.id
            doer = models.User.query.get(doer_id)
            if not doer:
                raise NoResultFound(doer_id, 'User')

        creator = models.User.query.get(task.creator.id)

        if not creator:
            raise NoResultFound(task.creator.id, 'User')

        if not models.TaskStatus.query.get(task.status.id):
            raise NoResultFound(task.status.id, 'TaskStatus')

        try:
            task_to_save = self.task_model(
                name=task.name,
                content=task.content,
                status_id=task.status.id,
                creator_id=task.creator.id,
                doer_id=doer_id
            )

            self.session.add(task_to_save)
            self.session.commit()

        except exc.IntegrityError as e:
            self.session.rollback()

            if 'unique' in str(e).lower():
                raise NotUnique('Task already exist')

            raise

        except exc.SQLAlchemyError:
            self.session.rollback()
            raise DbError()

        return self._to_domain_model(task_to_save)

    def delete(self, id):
        result = self.task_model.query.get(id)

        if not result:
            raise NoResultFound(id, Task.__name__)

        try:
            task = self._to_domain_model(result)
            self.session.delete(result)
            self.session.commit()

        except exc.IntegrityError as e:
            self.session.rollback()

            if 'foreign' in str(e).lower():
                raise CannotBeDeleted('Cannot delete task')
            raise

        except exc.SQLAlchemyError:
            self.session.rollback()
            raise DbError()

        return task

    def _to_domain_model(self, data):
        status = TaskStatus(id=data.status.id, name=data.status.name)

        creator = User(
            id=data.creator.id,
            name=data.creator.name,
            roles=[UserRole(id=role.id, name=role.name)
                   for role in data.creator.roles]
        )

        doer = None

        if data.doer:
            doer = User(
                id=data.doer.id,
                name=data.doer.name,
                roles=[UserRole(id=role.id, name=role.name)
                       for role in data.doer.roles]
            )

        return Task(
            name=data.name,
            content=data.content,
            status=status,
            creator=creator,
            doer=doer,
            id=data.id
        )

    def _parse_filters(self, filters=None):
        if not filters:
            return None

        filters = super()._parse_filters(filters)
        filters_expression = []

        for filter in filters:
            if filter.key == 'status_name':
                filters_expression.append(
                    self.task_model.status.has(name=filter.value))
            elif filter.key == 'creator_name':
                filters_expression.append(
                    self.task_model.creator.has(name=filter.value))
            elif filter.key == 'doer_name':
                filters_expression.append(
                    self.task_model.doer.has(name=filter.value))
            else:
                key = getattr(self.task_model, filter.key)
                filters_expression.append(
                    getattr(key, filter.operator)(filter.value))

        return filters_expression
