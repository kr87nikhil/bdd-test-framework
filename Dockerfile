# syntax=docker/dockerfile:1
FROM python:3.9-bullseye

LABEL version="2.0"
LABEL description="Create python 3.9 execution environment"
LABEL org.opencontainers.image.authors="nikhil1552@gmail.com"

RUN mkdir /python-bdd
COPY /setup.py /README.md /requirements.txt /python-bdd/
COPY /tests/app_aws/requirements.txt /python-bdd/tests/app_aws/
COPY /tests/database/requirements.txt /python-bdd/tests/database/

RUN pip install --upgrade pip
RUN pip install -e /python-bdd
RUN pip install -r /python-bdd/requirements.txt -r /python-bdd/tests/app_aws/requirements.txt -r /python-bdd/tests/database/requirements.txt

WORKDIR /python-bdd

CMD "pytest"
