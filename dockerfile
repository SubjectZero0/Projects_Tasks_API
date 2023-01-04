FROM python:3.11.1-alpine3.16

ENV PYTHONUNBUFFERED 1

COPY ./backend /dataverse_api
COPY ./requirements.txt /tmp/requirements.txt

WORKDIR /dataverse_api
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    chown -R django-user:django-user /dataverse_api && \
    chmod -R 755 /dataverse_api

ENV PATH="/py/bin:$PATH"

USER django-user