FROM python:3.7
FROM node:10

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD . /code/

RUN cd frontend/ && npm install

RUN pip install -r backend/requirements.txt