FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV TERM xterm
ENV PYTHONPATH /app
ENV GIT_SSL_NO_VERIFY=1

# update, upgrade, and install packages
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y apt-utils \
    && apt-get install -y curl git less man nano sudo wget \
    && apt-get install -y build-essential \
    && apt-get install -y libffi-dev gettext \
    && apt-get install -y postgresql-client

# configure apt-utils (fixes warnings)
RUN dpkg-reconfigure apt-utils

# set some useful defaults
RUN echo "alias ls='ls --color'" >> /etc/bash.bashrc
RUN echo "alias grep='grep --color=auto'" >> /etc/bash.bashrc

# update pip
RUN pip install --upgrade pip

# install ipython
RUN pip install ipython

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
