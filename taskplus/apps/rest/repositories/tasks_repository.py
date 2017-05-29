from taskplus.apps.rest import models
from taskplus.apps.rest.database import db_session
from taskplus.core.shared.repository import Repository
from taskplus.core.domain import Task, User, TaskStatus, UserRole


class TasksRepository(Repository):

    def __init__(self):
        self.task_model = models.Task
        self.session = db_session

    def one(self, id):
        result = self.task_model.query.filter_by(id=id).one()
        return self._to_domain_model(result)

    def list(self, filters=None):
        if not filters:
            result = self.task_model.query.all()
        else:
            filters = self._parse_filters(filters)
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

            result = self.task_model.query.filter(*filters_expression).all()

        return [self._to_domain_model(task) for task in result]

    def update(self, task):
        task_to_update = self.task_model.query.filter_by(id=task.id).one()
        task_to_update.status_id = task.status.id
        task_to_update.creator_id = task.creator.id
        task_to_update.doer_id = task.doer.id
        task_to_update.content = task.content
        task_to_update.name = task.name

        self.session.add(task_to_update)
        self.session.commit()

        return self._to_domain_model(task_to_update)

    def save(self, task):
        doer_id = None

        if task.doer:
            doer_id = task.doer.id

        task_to_save = self.task_model(
            name=task.name,
            content=task.content,
            status_id=task.status.id,
            creator_id=task.creator.id,
            doer_id=doer_id
        )

        self.session.add(task_to_save)
        self.session.commit()

        return self._to_domain_model(task_to_save)

    def delete(self, id):
        result = self.task_model.query.filter_by(id=id).one()
        task = self._to_domain_model(result)

        self.session.delete(result)
        self.session.commit()

        return task

    def _to_domain_model(self, data):
        status = TaskStatus(id=data.status.id, name=data.status.name)

        creator = User(
            id=data.creator.id,
            name=data.creator.name,
            role=UserRole(id=data.creator.role.id,
                          name=data.creator.role.name)
        )

        doer = None

        if data.doer:
            doer = User(
                id=data.doer.id,
                name=data.doer.name,
                role=UserRole(id=data.doer.role.id,
                              name=data.doer.role.name)
            )

        return Task(
            name=data.name,
            content=data.content,
            status=status,
            creator=creator,
            doer=doer,
            id=data.id
        )
