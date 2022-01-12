from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from database.utility.database_factory import DatabaseFactory


class SQLite3Factory(DatabaseFactory):
    """SQLite 3 database factory"""

    def db_name() -> str:
        return 'SQLite3'

    def create_database() -> Engine:
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
        return engine
