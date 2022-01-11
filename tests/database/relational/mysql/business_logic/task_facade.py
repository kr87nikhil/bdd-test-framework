from relational.mysql.business_logic.model.task import Task
from relational.mysql.business_logic.dao.task_dao import TaskDao


class TaskFacade:
    __task_dao: TaskDao

    def __init__(self, task_dao: TaskDao) -> None:
        self.__task_dao = task_dao

    def __is_task_associated(self, project_id: int, task: Task):
        associated_tasks = self.__task_dao.get_associated_tasks(project_id)
        if associated_tasks != None and task in associated_tasks:
            return True
        return False

    def get_task(self, task_id: int) -> Task:
        return self.__task_dao.get_task(task_id)

    def associate_task(self, project_id: int, task: Task) -> int:
        """Associate new task with project"""
        return self.__task_dao.get_task_id(project_id, task) if self.__is_task_associated(project_id, task)\
            else self.__task_dao.save_record(project_id, task)
