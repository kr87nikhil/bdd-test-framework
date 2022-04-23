import pytest
from pytest_bdd import given, when, then, scenarios
from pytest_bdd.parsers import parse

from non_relational.dynamo_db.business_logic.model.thing import Thing
from non_relational.dynamo_db.business_logic.thing_facade import ThingFacade
from non_relational.dynamo_db.persistence.dao_impl.thing_dao_impl import ThingDaoImpl


@pytest.fixture(scope='session')
def thing_facade():
    thing_dao = ThingDaoImpl()
    return ThingFacade(thing_dao)


scenarios('gateway_dynamoDB.feature')


@when(parse('POST HTTP request is triggered to {db_record} in {table_name}'))
def post_http_request_is_triggered_to_in(thing_facade: ThingFacade, db_record, table_name):
    thing_obj = Thing(db_record)
    thing_facade.create_thing(thing_obj, table_name)


@given(parse('{db_record} record should be available in {table_name}'))
@then(parse('same record should be available in DB'))
def record_should_be_available_in(thing_facade: ThingFacade, db_record, table_name):
    thing_obj = Thing(db_record)
    assert thing_facade.is_thing_exist(thing_obj, table_name), f'Thing {db_record} does not exist in {table_name}'
