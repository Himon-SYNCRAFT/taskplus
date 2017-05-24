from sqlalchemy import event, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from taskplus.core.domain import Statuses


engine = create_engine('sqlite:///data.db', echo=True, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def create_db():
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

    creator_role = models.UserRole(name='creator')
    doer_role = models.UserRole(name='doer')

    db_session.add(creator_role)
    db_session.add(doer_role)
    db_session.commit()

    creator = models.User(name='creator_1', role_id=creator_role.id)
    doer = models.User(name='doer_1', role_id=doer_role.id)

    db_session.add(creator)
    db_session.add(doer)
    db_session.commit()

    status_new = models.TaskStatus(id=Statuses.NEW.value, name='new')

    db_session.add(status_new)
    db_session.commit()

    task = models.Task(name='example task 1', content='lorem ipsum',
                       status_id=status_new.id, creator_id=creator.id,
                       doer_id=doer.id)

    db_session.add(task)
    db_session.commit()
