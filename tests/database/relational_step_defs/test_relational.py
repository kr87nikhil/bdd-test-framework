from pytest_bdd import scenarios
from database.relational_step_defs.core_steps import *
from database.relational_step_defs.orm_steps import *

scenarios('../features/relational.feature')

#conn.execute(text('select "hello world"'))
