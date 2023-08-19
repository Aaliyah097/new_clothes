# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.9

WORKDIR /flask_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ../requirements.txt .

RUN pip install -r requirements.txt

COPY .. /flask_app