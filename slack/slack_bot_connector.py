import os
import time
import requests

from bot_id_getter import bot_id_getter
from slackclient import SlackClient

# get SLACK_BOT_ID and SLACK_BOT_TOKEN as env variable
# min required is SLACK_BOT_TOKEN
BOT_ID = os.environ.get("SLACK_BOT_ID") if (os.environ.get("SLACK_BOT_ID")) else bot_id_getter("garybot")
AT_BOT = "<@" + BOT_ID + ">"


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    r = requests.get('http://nlp:5000/api/message/001/' + channel + '/' + command + '/').json()
    print r['response']['message']
    if r and 'response' in r and r['response']['message']:
        response = r['response']['message']
    else:
        response = "request error"
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].encode("utf8"), output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    if slack_client.rtm_connect():
        print("garybot connected, ready to handle command!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
