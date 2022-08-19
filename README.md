# Python - Behaviour Driven Development

- [Introduction](#introduction)
- [Pre-requisite](#pre-requisite)
  - [Python Installation](#1-python-37)
  - [Using Docker](#2-using-docker)
- [Usage](#usage)
  - Python Installation
  - Docker container
- [Debugging](#debugging)
- [Integration Coverage](#integration-coverage)
  - [Database](#database)
     - Relational
     - Non-Relational
  - [Web Service](#web-service)
- [External Report](#external-report)
  - [Allure](#allure)
  - [Report Portal](#report-portal)
  - [TestRail](#testrail)
- [Feedback](#feedback) - Please create issues to provide feedback!


## Introduction
Python test automation framework build for different integration testing.
`pytest-bdd` package is used to achieve BDD style test scenarios. 
It is built on top of `pytest` library.

**Why use pytest ?**
- Allows to run a standalone test function as its own case
- Automates test setup, teardown, and common test scenarios
- Great to use with CI tools like Travis, Jenkins, and Circle CI
- Actively maintained with a particularity open-source community

## Pre-requisite
### 1. Python 3.7
1. Windows
```cmd
$ python -m venv test_workspace --upgrade-deps
$ .\test_workspace\Scripts\activate
```
2. Linux
```bash
$ python3 -m virtualenv test_workspace
$ source test_workspace/bin/activate
```
Common:
```console
pip install --upgrade pip setuptools
pip install -e .
pip install -r requirements.txt -r ./tests/app_aws/requirements.txt -r ./tests/database/requirements.txt
```

### 2. Using Docker
These tests have been packaged to run with all dependencies installed within a Docker container.
To run, install docker and execute:
```bash
$ docker compose build
$ docker compose run test pip install .
```

## Usage
Generate Step definition
```bash
$ py.test --generate-missing --feature .\tests\app_aws\features .\tests\app_aws\step_defs
```

### Python installation
Run the test matching marker while printing all variables and verbose output
```bash
$ py.test -vvl -m "database"
```

Run the tests for a certain file matching a keyword
```bash
$ pytest -k <test_file_keyword>
```

### Docker solution
By default, Calculator test will be executed: `docker compose run test`

To execute another scenarios: `docker compose run test py.test -m "<module_name>"`


## Debugging

1. If you press `(ctrl + fn)`(VS Code) or `(Ctrl + F8)`(Pycharm IDE) within the debug output when running `pytest -vvl` or
when encountering test errors, your cursor may stick and be unable to continue 
writing in the docker shell. You can get past this by typing `q` to return to
entry mode in the docker container.


2. If you'd like to debug a piece of code, you can add the following built-in functions
   to a section of the code to enter into the pdb debugger while running pytest. 
   * `breakpoint()`

3. If you'd like to debug test case execution in docker container
```bash
$ docker compose run test -i
$ docker compose exec -it <container_name> sh
```

## Integration Coverage
### 1. Database
**Relational:**
The SQLAlchemy SQL Toolkit and Object Relational Mapper is a comprehensive set of tools for working databases with Python.

**Non-Relational:**
No-SQL database means not-only SQL, provides other programming construct to access data.

### 2. Web Service

[Go Rest](https://gorest.co.in/) - Online REST API for Testing

## External Report
### Allure
Allure Framework is a flexible lightweight multi-language test report tool.
It not only shows a very concise representation of what have been tested in a neat web report form, but allows everyone participating in the development process to extract maximum of useful information from everyday execution of tests.

From the managers perspective Allure provides a clear 'big picture' of what features have been covered, where defects are clustered, how the timeline of execution looks like and many other convenient things

Generate report:
`allure serve reports/<test_module>/tmp/allure_results`

**Reference:**
1. https://github.com/allure-framework/allure2
2. https://docs.qameta.io/allure/#_report_structure

### Report Portal
ReportPortal is a service, that provides increased capabilities to speed up results analysis and reporting through the use of built-in analytic features.
Report portal provides:
* Real-time integration
* Historical data of test execution
* AI-powered Test Automation Dashboard

For authentication, set environment variable:
* RP_UUID

**Reference**: https://github.com/reportportal/agent-python-pytest

### TestRail
TestRail is a web-based test case management tool.
It is used by testers, developers and team leads to manage, track, and organize software testing efforts.
TestRail allows team members to enter test cases, organize test suites, execute test runs, and track their results, all from a modern and easy to use web interface.

For authentication, set environment variable:
* TESTRAIL_ID
* TESTRAIL_KEY

## Feedback

I'd love to hear from you! 
Please make an issue on this repository, and I will get back to you. 