FROM python:3.11.1-alpine3.17

# set work directory
WORKDIR /usr/src/App

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update
RUN  apk add libpq build-base

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# lint
RUN pip install --upgrade pip

EXPOSE 15002

# copy project
COPY . .

