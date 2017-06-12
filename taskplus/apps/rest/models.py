import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table

from taskplus.apps.rest.database import Base


user_role_to_user = Table(
    'user_role_to_user', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('user_roles.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String(64), nullable=False)

    roles = relationship('UserRole', secondary=user_role_to_user)

    def __init__(self, name, password, roles, id=None):
        self.name = name
        self.password = self._hash_password(password)
        self.roles = roles
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
    name = Column(String, nullable=False, unique=True)


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
