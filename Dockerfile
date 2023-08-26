FROM python:3.9-slim AS builder

ARG RAR_VERSION=612

RUN apt-get update && \
    apt-get install curl -y && \
    curl -o /tmp/rar.tar.gz https://www.win-rar.com/fileadmin/winrar-versions/rarlinux-x64-${RAR_VERSION}.tar.gz && \
    cd /tmp && tar -xf rar.tar.gz



FROM python:3.9-slim-buster


COPY requirements.txt /tmp/

RUN mkdir /code /data /temp /config

WORKDIR /code


#COPY misc/unrar /usr/bin/unrar

ENV PYTHONPATH="/code/:/code/tasks/:${PATH}"
ENV DATA_PATH="/data"
ENV TEMP_PATH="/temp"

RUN mkdir /var/lib/luigi

COPY --from=builder /tmp/rar/unrar /usr/bin/unrar

RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

VOLUME /temp
VOLUME /data

COPY tasks /code/tasks
COPY tcomextetl /code/tcomextetl
COPY misc /code/misc
COPY settings.py /code/
COPY tasks_params.yml /code/tasks_params.yml

COPY conf/luigi.cfg /etc/luigi/luigi.cfg

ARG UNAME=airflow
ARG UID=50000
ARG GID=0

RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
USER $UNAME

EXPOSE 8082
