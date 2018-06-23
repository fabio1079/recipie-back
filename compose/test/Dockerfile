FROM python:3.6

RUN pip3 install --upgrade pip

RUN mkdir -p /app
WORKDIR /app

ADD . /app/
RUN pip3 install -r requirements/test.txt

ENV PYTHONUNBUFFERED 1
