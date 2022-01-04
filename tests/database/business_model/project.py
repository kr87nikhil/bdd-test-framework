from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from database import Base
# from database.business_model.reflected import Reflected


class Project(Base):
    """Project table mapped class"""
    __tablename__ = 'project'
    __table_args__ = {'schema': 'sqlAlchemy'}

    projectId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(30))
    description = Column(String)

    tasks = relationship('Task', back_populates='project')
