FROM python:3.6-alpine

RUN apk update \
  && apk add --no-cache --virtual build-deps gcc python3-dev musl-dev \
  && apk add --no-cache postgresql-dev

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY compose/api/entrypoint /entrypoint
RUN chmod +x /entrypoint

COPY compose/api/start /start
RUN chmod +x /start

WORKDIR /api

ENTRYPOINT ["/entrypoint"]
