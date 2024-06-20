FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /social_service

WORKDIR /social_service

ADD . /social_service/

RUN pip install -r requirements.txt
