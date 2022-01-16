import pytest
from app_aws.business_logic.thing_facade import ThingFacade
from app_aws.persistence.dynamo_db_dao_impl.thing_dao_impl import ThingDaoImpl


@pytest.fixture(scope='session')
def thing_facade():
    thing_dao = ThingDaoImpl()
    return ThingFacade(thing_dao)
