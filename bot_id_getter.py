import os
from slackclient import SlackClient


def bot_id_getter(bot_name):
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == bot_name:
                return user.get('id')
    return 0
