FROM python:3.6-alpine as base
FROM base as builder

RUN apk add --no-cache --update linux-headers musl-dev python-dev py-pip gcc git && rm -rf /var/cache/apk/*

COPY ./ /app
WORKDIR /app
RUN pip install -r ./requirements.txt

ENV GE_REPO_DIR=/app/repos

CMD ["python", "ge.py"]