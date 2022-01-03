import pytest
from database.utility.relational.mysql_factory import MySQLFactory
from database.utility.relational.sqlite3_factory import SQLite3Factory


def pytest_addoption(parser):
    """Define pytest command line parameters"""
    parser.addoption("--relational_db", action="store", default='SQLite3', help='Target database')


@pytest.fixture(scope='session')
def database_engine(request):
    database_name = request.config.getoption('relational_db')
    if database_name == MySQLFactory.db_name():
        engine = MySQLFactory.create_database()
    elif database_name == SQLite3Factory.db_name():
        engine = SQLite3Factory.create_database()
    return engine
