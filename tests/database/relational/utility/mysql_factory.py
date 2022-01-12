from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine

# from database.business_model.reflected import Reflected
from database.utility.database_factory import DatabaseFactory
from relational.utility.sql_script_reader import SqlScriptReader


class MySQLFactory(DatabaseFactory):
    """MySQL database factory"""
    
    def db_name() -> str:
        return 'MySQL'

    def create_database() -> Engine:
        engine = create_engine("mysql+mysqlconnector://test_user@localhost:3306", echo=True, future=True)
        MySQLFactory.initialize_database(engine)
        # Reflected.prepare(engine)
        return engine

    @staticmethod
    def initialize_database(engine) -> None:
        """Initialize sqlAlchemy database with seed data"""
        with Session(engine) as session:
            for script in SqlScriptReader():
                session.execute(text(script))
                session.commit()
