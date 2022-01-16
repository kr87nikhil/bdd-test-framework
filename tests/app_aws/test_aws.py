from pytest_bdd import scenarios
from app_aws.step_defs.gateway_dynamoDB_steps import *


scenarios("features/gateway_dynamoDB.feature")
