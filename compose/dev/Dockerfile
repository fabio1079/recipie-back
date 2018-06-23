FROM python:3.6

RUN pip3 install --upgrade pip

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip3 install -r requirements.txt

ADD . /app/

ENV PYTHONUNBUFFERED 1

# EXPOSE 8000
