ARG PYTHON_VERSION=3.12
FROM python:$PYTHON_VERSION-slim AS builder

ARG APP_HOME=/app
WORKDIR $APP_HOME

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV USE_DOCKER=True

# install dependencies system
ARG BUILD_DEPS="curl"
RUN apt-get update && apt-get install --no-install-recommends -y $BUILD_DEPS

RUN pip install --upgrade --no-cache-dir pip && \
	pip install --no-cache-dir poetry

# install dependencies
COPY pyproject.toml .

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes  && \
	pip install --no-cache-dir -r requirements.txt

# copy project
COPY ./app .
