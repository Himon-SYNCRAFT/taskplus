from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from taskplus.apps.rest.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role_id = Column(Integer, ForeignKey('user_roles.id'))

    role = relationship('UserRole')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    content = Column(String)
    status_id = Column(Integer, ForeignKey('task_statuses.id'))
    creator_id = Column(Integer, ForeignKey('users.id'))
    doer_id = Column(Integer, ForeignKey('users.id'))

    status = relationship('TaskStatus')
    creator = relationship('User', foreign_keys=[creator_id])
    doer = relationship('User', foreign_keys=[doer_id])


class TaskStatus(Base):
    __tablename__ = 'task_statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True)
    name = Column(String)
