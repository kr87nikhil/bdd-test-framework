from pytest_bdd import given, when, then, parsers

from tests.utility.parse_steps import StepTable
from relational.mysql.business_logic.model.task import Task
from relational.mysql.business_logic.model.project import Project
from relational.mysql.business_logic.task_facade import TaskFacade
from relational.mysql.business_logic.project_facade import ProjectFacade

@given(
    parsers.parse('project need to be completed\n{step_table_dict:static_fields}'),
    extra_types=dict(static_fields=StepTable.parse_nested_key_step_table),
    target_fixture='project_id'
)
def project_need_to_be_completed(project_facade: ProjectFacade, step_table_dict):
    """Insert data in project table if not exist"""
    project_title = step_table_dict.get('project_title')
    project_description = step_table_dict.get('project_description')
    project_obj = Project(title=project_title, description=project_description)
    return project_facade.create_project(project_obj)

@when(
    parsers.parse('task with {task_description} need to be completed'),
    target_fixture='task_id'
)
def task_need_to_be_completed(task_facade: TaskFacade, project_id, task_description):
    """Add task to the selected project"""
    task_obj = Task(task_description)
    return task_facade.associate_task(project_id, task_obj)

@then('task details should be persisted in the DB')
def task_details_should_be_persisted_in_the_db(task_facade: TaskFacade, task_description, task_id):
    task = task_facade.get_task(task_id)
    assert task != None and task == Task(task_description), 'Created task description should match'
