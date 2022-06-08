FROM python:alpine as builder

WORKDIR /app


RUN pip install pipenv  && \
    apk add gcc g++ python3-dev libffi-dev

ENV PIPENV_VENV_IN_PROJECT=1

ADD Pipfile* .
RUN pipenv install --skip-lock


FROM python:alpine as test

WORKDIR /app


ENV PIPENV_VENV_IN_PROJECT=1
RUN pip install pipenv

COPY --from=builder /app/ /app/
RUN pipenv install --dev --skip-lock

ADD app /app/app
ADD assets /app/assets
ADD pytest.ini /app/pytest.ini

CMD pipenv run pytest app


FROM python:alpine as prod

WORKDIR /app


ENV PIPENV_VENV_IN_PROJECT=1
RUN pip install pipenv

COPY --from=builder /app/ /app/

ADD app /app/app

CMD pipenv run python -m app
