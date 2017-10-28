FROM python:2.7
MAINTAINER victorbalssa <balssa_v@etna-alternance.net>

ADD ./requirements.txt /bot/requirements.txt
WORKDIR /bot
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./slack_bot_connector.py"]
