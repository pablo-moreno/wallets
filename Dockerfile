FROM python:3.9-slim

WORKDIR /app
COPY . /app

ARG VERSION
ENV APP_VERSION=$VERSION

RUN apt-get update && apt-get install -y gcc vim postgresql-client

RUN pip install -r requirements.txt
