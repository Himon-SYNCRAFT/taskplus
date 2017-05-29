from taskplus.apps.rest import models
from taskplus.apps.rest.database import db_session
from taskplus.core.domain import TaskStatus
from taskplus.core.shared.repository import Repository


class TaskStatusesRepository(Repository):

    def __init__(self):
        self.status_model = models.TaskStatus
        self.session = db_session

    def one(self, id):
        status = self.status_model.query.filter_by(id=id).one()
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
        status_to_update = self.status_model.query.filter_by(id=status.id).one()
        status_to_update.name = status.name

        self.session.add(status_to_update)
        self.session.commit()

        return TaskStatus(id=status_to_update.id, name=status_to_update.name)

    def save(self, status):
        new_status = self.status_model(name=status.name)

        self.session.add(new_status)
        self.session.commit()

        return TaskStatus(id=new_status.id, name=new_status.name)

    def delete(self, id):
        status = self.status_model.query.filter_by(id=id).one()
        self.session.delete(status)
        self.session.commit()

        return TaskStatus(id=id, name=status.name)
