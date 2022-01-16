from abc import ABC, abstractmethod
from typing import List
from tests.app_aws.business_logic.model.thing import Thing


class ThingDao(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_things(self, table_name: str) -> List[Thing]:
        pass
