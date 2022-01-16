import logging
from typing import List
from boto3 import client
from botocore.client import BaseClient, ClientError

from app_aws import my_config
from app_aws.business_logic.model.thing import Thing
from app_aws.business_logic.dao.thing_dao import ThingDao


class ThingDaoImpl(ThingDao):
    DB_NAME = 'dynamodb'
    __dynamodb_client: BaseClient

    def __init__(self) -> None:
        try:
            self.__dynamodb_client = client(self.DB_NAME, config=my_config)
        except ClientError as error:
            logging.log(level=logging.CRITICAL, msg='Unable to create dynamoDB client')
            raise error
    
    def get_things(self, table_name: str) -> List[Thing]:
        try:
            table_items = self.__dynamodb_client.scan(
                TableName = table_name
            )
            things_records = list()
            for item in table_items.get('Items'):
                things_records.append(Thing(item.get('thingId').get('S')))
            return things_records
        except ClientError as error:
            logging.log(level=logging.ERROR, msg=error)
