# python-bdd

- [Introduction](#introduction)
- [Prerequisite](#prerequisite)
- [Usage](#usage)
- [Debugging](#debugging)
- [Integration Coverage](#integration-coverage)
  - [Database](#database)
     - Relational
     - Non-Relational
  - [Web Service](#web-service)
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

## Prerequisite
**1. Run from Terminal**

Already installed Python 3.9 or above
```bash
$ python3.10 -m venv test_workspace --upgrade-deps
$ .\test_workspace\Scripts\activate
$ pip install -e .
$ pip install -r requirements.txt
```

**2. Run using Docker**

These tests have been packaged to run with all dependencies installed within a Docker container.
To run install docker and open a shell:
```bash
$ docker-compose build
$ docker-compose run test sh
```

This will open the docker shell.

## Usage
  
**Run the test matching marker**
```bash
$ pytest 
```

**Run the tests for a certain file matching a keyword**
```bash
$ pytest -k <test_file_name>
```

**Run tests while printing all variables and verbose output**
```bash
$ pytest -vvl
```

**To exit the shell**
```bash
$ exit
```

## Debugging

1. If you press `(ctrl + fn)`(VS Code) or `(Ctrl + F8)`(Pycharm IDE) within the debug output when running `pytest -vvl` or
when encountering test errors, your cursor may stick and be unable to continue 
writing in the docker shell. You can get past this by typing `q` to return to
entry mode in the docker container.


2. If you'd like to debug a piece of code, you can add the following built-in functions
   to a section of the code to enter into the pdb debugger while running pytest. 
   * `breakpoint()`

## Integration Coverage
### Database
**Relational:**
The SQLAlchemy SQL Toolkit and Object Relational Mapper is a comprehensive set of tools for working databases with Python.

**Non-Relational:**
No-SQL database means not-only SQL, provides other programming construct to access data.

### Web Service

[Go Rest](https://gorest.co.in/) - Online REST API for Testing

## Feedback

I'd love to hear from you! 
Please make an issue on this repository, and I will get back to you. 