FROM python:3.9-slim-buster

WORKDIR /tcomextetl

#ENV LUIGI_CONFIG_PARSER=toml

COPY requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY ./tasks ./tasks
COPY ./tcomextdata ./tcomextdata
COPY ./settings.py ./settings.py
RUN mkdir /var/lib/luigi

EXPOSE 8082
