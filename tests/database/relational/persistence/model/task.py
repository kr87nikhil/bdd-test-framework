from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from tests.database.relational import Base
# from database.relational.persistence.reflected import Reflected


class Task(Base):
    """Task table mapped class"""
    __tablename__ = 'task'
    __table_args__ = {'schema': 'sqlAlchemy'}

    taskId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    description = Column(String)
    projectId = Column(Integer, ForeignKey('sqlAlchemy.project.projectId'))

    project = relationship('Project', back_populates='tasks')
