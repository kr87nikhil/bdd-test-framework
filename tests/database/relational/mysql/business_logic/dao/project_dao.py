from abc import ABC, abstractmethod
from relational.mysql.business_logic.model.project import Project


class ProjectDao(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_project(self, title: str) -> Project:
        pass

    @abstractmethod
    def get_project_id(self, title: str) -> int:
        pass

    @abstractmethod
    def save_record(self, project: Project) -> int:
        pass
