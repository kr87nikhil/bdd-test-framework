# syntax=docker/dockerfile:1
FROM python:3.9-bullseye

LABEL version="2.0"
LABEL description="Python 3.9 execution environment"
LABEL org.opencontainers.image.authors="nikhil1552@gmail.com"

WORKDIR pytest_bdd
COPY /setup.py /README.md /requirements.txt ./
COPY /tests/app_aws/requirements.txt ./tests/app_aws/
COPY /tests/database/requirements.txt ./tests/database/

RUN pip install virtualenv
RUN python3 -m virtualenv test_workspace
RUN /bin/bash -c '. test_workspace/bin/activate; \
pip install --upgrade pip setuptools; \
pip install -r ./requirements.txt -r ./tests/app_aws/requirements.txt -r ./tests/database/requirements.txt'

WORKDIR ../python-bdd
CMD ["/bin/bash", "-c", ". ../pytest_bdd/test_workspace/bin/activate; pip install ."]
