FROM python:3.6 as base
FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local
COPY ./ /app

WORKDIR /app

ENV GE_REPO_DIR=/app/repos

CMD ["python", "ge.py"]