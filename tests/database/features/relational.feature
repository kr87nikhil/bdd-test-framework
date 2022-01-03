@database @relational
Feature: Relational Database testing via SQLAlchemy
    As a global publishing house of Movies publishing company
    I want to add few movie details
    So that movie details become persisten in database

@SQLite3
@jira(Test-563)
Scenario Outline: Core operations
    When Movies table is created
    And <movie_name> directed by <director> is published on <year> is added
    Then movie should be persisted in the DB

    Examples:
        | movie_name         | director          | year |
        | Pulp Fiction       | Quentin Tarantino | 1994 |
        | Back to the Future | Steven Spielberg  | 1985 |
        | Moonrise Kingdom   | Wes Anderson      | 2012 |

@todo
@MySQL
@jira(Test-571)
Scenario Outline: ORM operations
    Given project need to be completed 
    #     | field               | value           |
    #     | project_title       | Clean house     |
    #     | project_description | Clean by room   |
    When task with <task_description> need to be completed
    Then task details should be persisted in the DB

    Examples:
        | task_description      |
        | Kitchen cleaning      |
        | Bathroom cleaning     |
        | Living room cleaning  | 
