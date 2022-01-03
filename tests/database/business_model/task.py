from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from database import Base
from database.business_model.reflected import Reflected


class Task(Reflected, Base):
    """Task table mapped class"""
    __tablename__ = 'Task'

    project_id = Column(Integer, ForeignKey('Project.project_id'))
