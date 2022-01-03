from sqlalchemy.orm import relationship
from database import Base
from database.business_model.reflected import Reflected


class Project(Reflected, Base):
    """Project table mapped class"""
    __tablename__ = 'Project'

    tasks = relationship("Task")
