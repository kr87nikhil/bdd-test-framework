import pytest
from relational.mysql.business_logic.task_facade import TaskFacade
from relational.mysql.business_logic.project_facade import ProjectFacade
from relational.mysql.persistence.dao_impl.task_dao_impl import TaskDaoImpl
from relational.mysql.persistence.dao_impl.project_dao_impl import ProjectDaoImpl


@pytest.fixture(scope='session')
def project_facade(database_engine):
    project_dao = ProjectDaoImpl(database_engine)
    return ProjectFacade(project_dao)

@pytest.fixture(scope='session')
def task_facade(database_engine):
    task_dao = TaskDaoImpl(database_engine)
    return TaskFacade(task_dao)
