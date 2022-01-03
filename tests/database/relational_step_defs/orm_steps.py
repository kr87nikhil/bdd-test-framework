from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import insert, select
from pytest_bdd import given, when, then, parsers

from database.business_model.project import Project
from database.business_model.task import Task

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
        result = session.execute(select_stmt).all()
        if len(result) == 0:
            insert_stmt = insert(Project).values(
                title = project_title, description = project_description
            ).compile()
            insert_result = session.execute(insert_stmt)
            session.commit()
            return insert_result.inserted_primary_key[0]
        else:
            return result[0].project_id

@when(
    parsers.parse('task with {task_description} need to be completed'),
    target_fixture='task_id'
)
def task_need_to_be_completed(database_engine, project_id, task_description):
    """Add task to the selected project"""
    select_stmt = select(Task).where(
        Task.project_id == project_id, Task.description == task_description
    )
    insert_stmt = insert(Task).values(
        project_id = project_id, description = task_description
    ).compile()
    with Session(database_engine) as session:
        result = session.execute(select_stmt).all()
        if len(result) == 1:
            return result[0].task_id
        insert_result = session.execute(insert_stmt)
        session.commit()
        return insert_result.inserted_primary_key

@then('task details should be persisted in the DB')
def task_details_should_be_persisted_in_the_db(database_engine, task_description, task_id):
    select_stmt = select(Task).where(Task.task_id == task_id)
    with Session(database_engine) as session:
        result = session.execute(select_stmt).all()
        assert len(result) == 1, 'There should be atmost 1 newly added task'
        assert result[0].task_description == task_description, 'Created task description should match'
