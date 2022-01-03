from abc import ABC, abstractclassmethod


class DatabaseFactory(ABC):
    """Database factory for database connection"""

    def __init__(self) -> None:
        super.__init__()        

    @property
    @abstractclassmethod
    def db_name():
        """Database name"""
        pass

    @abstractclassmethod
    def create_database():
        """Get database engine"""
        pass
