from typing import List
from relational.mysql.business_logic.model.task import Task


class Project:
    title: int
    description: str
    tasks: List[Task]

    def __init__(self, title, description) -> None:
        self.title = title
        self.description = description
