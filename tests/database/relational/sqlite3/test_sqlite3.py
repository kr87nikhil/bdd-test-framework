from pytest_bdd import scenarios
from relational.sqlite3.step_defs.sqlite3_core_steps import *


scenarios('features/sqlite3.feature')

#conn.execute(text('select "hello world"'))