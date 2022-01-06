from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import insert, select
from pytest_bdd import given, when, then, parsers

from tests.database.relational.persistence.model.project import Project
from tests.database.relational.persistence.model.task import Task

@given(
    parsers.parse('project need to be completed'),
    target_fixture='project_id'
)
def project_need_to_be_completed(database_engine):
    """Insert data in project table if not exist"""
    project_title = 'Clean house'
    project_description = 'Clean by room'
    with Session(database_engine) as session:
        select_stmt = select(Project).where(Project.title == project_title)
        result = session.execute(select_stmt).first()
        if result == None:
            insert_stmt = insert(Project).values(
                title = project_title, description = project_description
            )
            insert_result = session.execute(insert_stmt)
            session.commit()
            return insert_result.inserted_primary_key[0]
        else:
            return result[0].projectId

@when(
    parsers.parse('task with {task_description} need to be completed'),
    target_fixture='task_id'
)
def task_need_to_be_completed(database_engine, project_id, task_description):
    """Add task to the selected project"""
    select_stmt = select(Task).where(
        Task.projectId == project_id, Task.description == task_description
    )
    insert_stmt = insert(Task).values(
        projectId = project_id, description = task_description
    )
    with Session(database_engine) as session:
        result = session.execute(select_stmt).first()
        if result != None:
            return result[0].taskId
        insert_result = session.execute(insert_stmt)
        session.commit()
        return insert_result.inserted_primary_key

@then('task details should be persisted in the DB')
def task_details_should_be_persisted_in_the_db(database_engine, task_description, task_id):
    select_stmt = select(Task).where(Task.taskId == task_id)
    with Session(database_engine) as session:
        result = session.execute(select_stmt).first()
        assert result[0].description == task_description, 'Created task description should match'
