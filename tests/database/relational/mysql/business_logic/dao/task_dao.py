from abc import ABC, abstractmethod
from typing import List
from relational.mysql.business_logic.model.task import Task


class TaskDao(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_task(self, task_id: int) -> Task:
        pass

    @abstractmethod
    def get_task_id(self, project_id: int, task: Task) -> int:
        pass

    @abstractmethod
    def get_associated_tasks(self, project_id: int) -> List[Task]:
        pass

    @abstractmethod
    def save_record(self, project_id: int, task: Task) -> int:
        pass
