FROM python:3.6-slim

RUN pip install pipenv==11.6.1

ENV PIPENV_VENV_IN_PROJECT=True
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY Pipfile.lock /opt/app/
COPY Pipfile /opt/app/
RUN cd /opt/app/ && pipenv install

COPY . /opt/app/
WORKDIR /opt/app

ENV ENVIRONMENT=dev
# pipenv run python manage.py runserver 0.0.0.0:3720 --settings slack.settings.dev