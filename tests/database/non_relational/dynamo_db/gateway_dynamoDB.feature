Feature: AWS API gateway integration
  As a user AWS application
  I want to trigger HTTP request to AWS API gateway endpoint
  So that corresponding unique records added into Dynamo DB

  @jira(Test-967)
  Scenario Outline: Validate record in Dynamo DB
    Given <db_record> record should be available in things

  Examples:
  | db_record    |
  | consoletest  |
  | lambdatest   |
  | frontendtest |


  @jira(Test-826)
  Scenario Outline: Create record in Dynamo DB
    When POST HTTP request is triggered to <db_record> in things
    Then same record should be available in DB

  Examples:
  | db_record                 |
  | gateway_integration_test  |
  | dynamoDB_integration_test |
