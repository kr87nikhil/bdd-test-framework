# syntax=docker/dockerfile:1
FROM python:3.9-bullseye AS test

LABEL image.author="Nikhil Kumar"

RUN mkdir /pytest_project/
COPY ./requirements.txt /pytest_project/
COPY ./setup.py ./setup.py

RUN pip install --upgrade pip setuptools
RUN pip install -e .
RUN pip install -r /pytest_project/requirements.txt

WORKDIR /pytest_project/

CMD "pytest"
ENV PYTHONDONTWRITEBYTECODE=true
