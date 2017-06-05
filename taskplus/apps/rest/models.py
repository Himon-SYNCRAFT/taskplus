import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from taskplus.apps.rest.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String(64), nullable=False)
    role_id = Column(Integer, ForeignKey('user_roles.id'), nullable=False)

    role = relationship('UserRole')

    def __init__(self, name, password, role_id, id=None):
        self.name = name
        self.password = self._hash_password(password)
        self.role_id = role_id
        self.id = id

    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    status_id = Column(Integer,
                       ForeignKey('task_statuses.id'), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    doer_id = Column(Integer, ForeignKey('users.id'))

    status = relationship('TaskStatus')
    creator = relationship('User', foreign_keys=[creator_id])
    doer = relationship('User', foreign_keys=[doer_id])


class TaskStatus(Base):
    __tablename__ = 'task_statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
