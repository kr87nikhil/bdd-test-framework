from database.utility.database_factory import DatabaseFactory
from database.relational.utility.mysql_factory import MySQLFactory
from database.relational.utility.sqlite3_factory import SQLite3Factory


class DatabaseContext:
    __database_factory: DatabaseFactory
    __available_implementations = [MySQLFactory, SQLite3Factory]

    def set_database(self, name: str):
        for database_factory in self.__available_implementations:
            if database_factory.db_name() == name:
                self.__database_factory = database_factory
        if self.__database_factory is None:
            raise Exception("Database implementation not found")

    def get_database_engine(self):
        return self.__database_factory.create_database()
