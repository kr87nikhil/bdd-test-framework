# syntax=docker/dockerfile:1
FROM python:3.7-alpine

LABEL version="1.0"
LABEL description="Python 3.7 execution environment"
LABEL org.opencontainers.image.authors="nikhil1552@gmail.com"

RUN pip3 install virtualenv
RUN pip3 install --upgrade pip setuptools

WORKDIR /usr/src/app
RUN python3 -m virtualenv test_workspace

ENV PATH="/usr/src/app/test_workspace/bin:$PATH"

COPY /setup.py /README.md /requirements.txt ./
COPY /tests/app_aws/requirements.txt ./tests/app_aws/
COPY /tests/database/requirements.txt ./tests/database/

RUN pip3 install -r ./requirements.txt -r ./tests/app_aws/requirements.txt -r ./tests/database/requirements.txt

ENTRYPOINT ["python3", "-m"]
CMD ["py.test", "-k", "calculator"]
