from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from database import Base
from database.business_model.project import Project
# from database.business_model.reflected import Reflected


class Task(Base):
    """Task table mapped class"""
    __tablename__ = 'task'
    __table_args__ = {'schema': 'sqlAlchemy'}

    taskId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    description = Column(String)
    projectId = Column(Integer, ForeignKey(Project.__table__.c.projectId))

    project = relationship('Project', back_populates='tasks')
