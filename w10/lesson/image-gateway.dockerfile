FROM python:3.11.0-slim

RUN pip install pipenv

WORKDIR /app

COPY Pipfile* ./

RUN pipenv install --system --deploy

COPY gateway.py protobuf.py ./

EXPOSE 9696

ENTRYPOINT gunicorn --bind=0.0.0.0:9696 gateway:app