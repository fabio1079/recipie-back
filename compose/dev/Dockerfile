FROM python:3.7

RUN pip3 install --upgrade pip

RUN mkdir -p /app
WORKDIR /app

ADD . /app/
RUN pip3 install -r requirements/dev.txt

ENV PYTHONUNBUFFERED 1
