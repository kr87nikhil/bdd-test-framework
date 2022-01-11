from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.expression import insert, select

from typing import List
from relational.mysql.business_logic.model.task import Task
from relational.mysql.business_logic.dao.task_dao import TaskDao
from relational.mysql.persistence.model.task import Task as TaskDB


class TaskDaoImpl(TaskDao):
    __engine: Engine

    def __init__(self, database_engine) -> None:
        self.__engine = database_engine

    def get_task(self, task_id: int) -> Task:
        select_task = select(TaskDB.description).filter_by(taskId=task_id)
        with Session(self.__engine) as session:
            result = session.execute(select_task).first()
        return Task(task_description=result[0]) if result != None else None

    def get_task_id(self, project_id: int, task: Task) -> int:
        select_task_id = select(TaskDB.taskId).filter_by(
            projectId=project_id, description=task.description
        )
        with Session(self.__engine) as session:
            result = session.execute(select_task_id).first()
        return result[0] if result != None else None

    def get_associated_tasks(self, project_id: int) -> List[Task]:
        select_associated_task = select(TaskDB).filter_by(projectId=project_id)
        with Session(self.__engine) as session:
            result = session.execute(select_associated_task).first()
        return [Task(description) for description in
                [task_db.description for task_db in result]]

    def save_record(self, project_id: int, task: Task) -> int:
        insert_task = insert(TaskDB).values(
            projectId = project_id, description = task.description
        )
        with Session(self.__engine) as session:
            result = session.execute(insert_task)
            session.commit()
        return result.inserted_primary_key[0]
