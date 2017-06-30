FROM debian:jessie
MAINTAINER nandotk <victor@dekalee.fr>

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    python2.7 \
    python-pip \
    build-essential \
    python-dev

ADD ./requirements.txt /bot/requirements.txt
WORKDIR /bot
RUN pip install -r requirements.txt
