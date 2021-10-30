Feature: Calculator
  As a user of calculator application
  I want to perform basic operations
  So that able to get result and history of all operations

  @jira(Test-253)
  Scenario Outline: All available operation
    When <first_number> is operated with <operation> by <second_number>
    Then result should be <expected_result>

  Examples:
    | first_number | operation      | second_number | expected_result |
    | 10           | ADDITION       | 93.7253       | 103.7253        |
    | 1965         | ADDITION       | 3654025       | 3655990         |
    | 9864         | SUBTRACTION    | 78536         | -68672          |
    | 4546         | SUBTRACTION    | 343.72        | 4202.28         |
    | 4.6333       | MULTIPLICATION | 83.29         | 385.907557      |
    | 51686        | MULTIPLICATION | 6454          | 333581444       |
    | 103          | DIVISION       | 2             | 51.5            |
    | 27.0         | DIVISION       | 3             | 9.0             |



  @jira(Test-254)
  Scenario Outline: With one negative number
    When <first_number> is operated with <operation> by <second_number>
    Then result should be <expected_result>

  Examples:
    | first_number | operation      | second_number | expected_result     |
    | -2           | ADDITION       | 832.9999      | 830.9999            |
    | 32           | SUBTRACTION    | -96           | 128                 |
    | -629         | MULTIPLICATION | 27            | -16983              |
    | 4689         | DIVISION       | -33           | -142.09090909090909 |
