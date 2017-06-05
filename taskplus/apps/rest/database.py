import os
from sqlalchemy import event, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from taskplus.core.domain import Statuses
from taskplus.apps.rest.settings import ProdConfig, DevConfig, TestConfig


if os.environ.get('TESTING'):
    config = TestConfig
elif os.environ.get('PRODUCTION'):
    config = ProdConfig
else:
    config = DevConfig

db_uri = config.DB_URI

engine = create_engine(db_uri, echo=False, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def create_db():
    # turn on foreign keys
    if db_session.bind.driver == 'pysqlite':
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    from taskplus.apps.rest import models
    Base.metadata.reflect(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    creator_role = models.UserRole(name='creator_role')
    doer_role = models.UserRole(name='doer_role')

    db_session.add(creator_role)
    db_session.add(doer_role)
    db_session.commit()

    creator = models.User(name='creator', role_id=creator_role.id,
                          password='creator')
    doer = models.User(name='doer', role_id=doer_role.id, password='doer')

    db_session.add(creator)
    db_session.add(doer)
    db_session.commit()

    status_new = models.TaskStatus(id=Statuses.NEW, name='new')
    status_in_progress = models.TaskStatus(
        id=Statuses.IN_PROGRESS, name='in progress')
    status_completed = models.TaskStatus(
        id=Statuses.COMPLETED, name='completed')
    status_canceled = models.TaskStatus(
        id=Statuses.CANCELED, name='canceled')

    db_session.add(status_new)
    db_session.add(status_in_progress)
    db_session.add(status_completed)
    db_session.add(status_canceled)
    db_session.commit()

    task = models.Task(name='example task 1', content='lorem ipsum',
                       status_id=status_new.id, creator_id=creator.id,
                       doer_id=doer.id)

    task2 = models.Task(name='example task 2', content='lorem ipsum2',
                        status_id=status_completed.id, creator_id=creator.id,
                        doer_id=doer.id)

    db_session.add(task)
    db_session.add(task2)
    db_session.commit()
