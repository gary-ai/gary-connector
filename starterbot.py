
import os
import time
import requests
from slackclient import SlackClient

# get BOT_ID and SLACK_BOT_TOKEN as env variable
BOT_ID = os.environ.get("BOT_ID")
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# constants
AT_BOT = "<@" + BOT_ID + ">"
ADMIN_ID = "****"


def call_api_test(api, url):
    """
        call api test
    """
    url = "http://" + url + ":5000/api/" + api
    response = requests.get(url)
    return response.content


def handle_command(command, channel, user):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the help command (@garybot help) to get started with Gary."
    if command.startswith("help"):
        response = "Command list:\n @garybot up somfy : Open somfy rolling\n" \
                   "@garybot down somfy : Down somfy rolling\n" \
                   "@garybot stop somfy : Stop somfy rolling\n"
    elif command.startswith("up somfy") and user == ADMIN_ID:
        response = "done. " + call_api_test("up", "******")
    elif command.startswith("down somfy") and user == ADMIN_ID:
        response = "done. " + call_api_test("down", "******")
    elif command.startswith("stop somfy") and user == ADMIN_ID:
        response = "done. " + call_api_test("stop", "******")
    elif command.startswith("open somfy") and user != ADMIN_ID:
        response = "Unauthorized."
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
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel'], output['user']
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel and user:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
