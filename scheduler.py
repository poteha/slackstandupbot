import json
import os
from urllib.request import urlopen

SCHEDULER_URL = os.environ.get('SCHEDULER_URL')
REMINDER_URL = os.environ.get('REMINDER_URL')


def return_200_wrapper(payload=None):
    if payload is None:
        payload = {}
    return {
        'statusCode': 200,
        'body': json.dumps(payload)
    }


def handler(event, context):
    r = urlopen(SCHEDULER_URL)
    print(r.read())
    return return_200_wrapper()


def handler_reminder(event, context):
    r = urlopen(REMINDER_URL)
    print(r.read())
    return return_200_wrapper()
