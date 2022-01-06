from pytest_bdd import scenarios
from tests.database.relational.step_defs.sqlite3_core_steps import *
from tests.database.relational.step_defs.mysql_orm_steps import *

scenarios('features/mysql.feature')

#conn.execute(text('select "hello world"'))
