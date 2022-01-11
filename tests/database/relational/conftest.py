import pytest
from relational.utility.mysql_factory import MySQLFactory
from relational.utility.sqlite3_factory import SQLite3Factory


@pytest.fixture(scope='session')
def database_engine(request):
    database_name = request.config.getoption('relational_db')
    if database_name == MySQLFactory.db_name():
        engine = MySQLFactory.create_database()
    elif database_name == SQLite3Factory.db_name():
        engine = SQLite3Factory.create_database()
    return engine
