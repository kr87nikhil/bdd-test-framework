@database @relational @SQLite3
Feature: Relational Database testing via SQLAlchemy
    As a global publishing house of Movies publishing company
    I want to add few movie details
    So that movie details become persisten in database

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
