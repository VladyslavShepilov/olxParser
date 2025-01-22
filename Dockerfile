FROM python:3.12.2-alpine

ENV PYTHOUNBUFFERED 1

WORKDIR /olx_parser

RUN apt-get update && apt-get -y install gcc mono-mcs libpq-dev wget unzip apt-transport-https ca-certificates curl gnupg


RUN apk add --no-cache \
    bash \
    chromium \
    chromium-chromedriver \
    build-base \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    openssl-dev \
    postgresql-dev \
    musl-dev \
    py3-pip \
    py3-cffi \
    tzdata \
    openjdk11-jre \
    git

ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
COPY .env_sample .env

EXPOSE 8000

RUN mkdir -p /var/olx_parser/tmp && chmod -R 777 /var/olx_parser

CMD ["python", "main.py"]