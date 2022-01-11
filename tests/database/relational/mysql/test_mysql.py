from pytest_bdd import scenarios
from relational.mysql.step_defs.mysql_steps import *


scenarios('features/mysql.feature')
