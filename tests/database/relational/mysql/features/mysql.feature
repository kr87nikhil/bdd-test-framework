Feature: MySQL database testing using SQLAlchemy ORM
    # TODO: Meaningful description

@todo
@MySQL
@jira(Test-571)
Scenario Outline: ORM operations
    Given project need to be completed
         | project_title       | Clean house     |
         | project_description | Clean by room   |
    When task with <task_description> need to be completed
    Then task details should be persisted in the DB

    Examples:
        | task_description      |
        | Kitchen cleaning      |
        | Bathroom cleaning     |
        | Living room cleaning  | 
