# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev cargo
RUN pip install psycopg2-binary

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./dist ./dist

RUN pip install ./dist/*tar.gz

# copy project
COPY . .

