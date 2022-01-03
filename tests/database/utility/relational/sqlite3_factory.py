from sqlalchemy import create_engine
from database.utility.database_factory import DatabaseFactory


class SQLite3Factory(DatabaseFactory):
    """SQLite 3 database factory"""

    def db_name():
        return 'SQLite3'

    def create_database():
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
        return engine
