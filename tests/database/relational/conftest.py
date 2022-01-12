import pytest
from database.utility.database_strategy import DatabaseContext


@pytest.fixture(scope='session')
def database_engine(request):
    database_name = request.config.getoption('relational_db')
    db_context = DatabaseContext()
    db_context.set_database(database_name)
    return db_context.get_database_engine()
