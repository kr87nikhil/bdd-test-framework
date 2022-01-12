from abc import ABC, abstractclassmethod
from sqlalchemy.engine.base import Engine


class DatabaseFactory(ABC):
    """Database factory for database connection"""

    def __init__(self) -> None:
        super.__init__()        

    @property
    @abstractclassmethod
    def db_name() -> str:
        """Database name"""
        pass

    @abstractclassmethod
    def create_database() -> Engine:
        """Get database engine"""
        pass
