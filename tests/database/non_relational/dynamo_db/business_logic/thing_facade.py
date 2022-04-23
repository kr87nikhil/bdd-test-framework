from os import getenv, path
from requests import post
from non_relational.dynamo_db.business_logic.model.thing import Thing
from non_relational.dynamo_db.business_logic.dao.thing_dao import ThingDao


class ThingFacade:
    __base_url: str = getenv('AWS_GATEWAY_BASE_URL')
    __thing_dao: ThingDao

    def __init__(self, thing_dao: ThingDao) -> None:
        self.__thing_dao = thing_dao

    @staticmethod
    def __get_request_payload(thing: Thing, table_name: str):
        return {
            'TableName': table_name,
            'Item': {
                'thingId': thing.creation_instance
            }
        }

    def is_thing_exist(self, thing: Thing, table_name: str):
        """Check if record exist in things table"""
        thing_records = self.__thing_dao.get_things(table_name)
        return True if thing in thing_records else False

    def create_thing(self, thing: Thing, table_name: str):
        """Save thing if not added"""
        if not self.is_thing_exist(thing, table_name):
            response = post(path.join(self.__base_url, 'serverlessWebAppCRUD'),
                            json=self.__get_request_payload(thing, table_name))
            response.raise_for_status()
