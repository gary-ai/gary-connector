FROM debian:jessie
MAINTAINER victorbalssa <balssa_v@etna-alternance.net>

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
