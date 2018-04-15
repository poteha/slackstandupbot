from urllib.request import urlopen
import json
import os

URL = os.environ.get('SCHEDULER_URL')

def return_200_wrapper(payload=None):
    if payload is None:
        payload = {}
    return {
        'statusCode': 200,
        'body': json.dumps(payload)
    }


def handler(event, context):
    r = urlopen(URL)
    print(r.read())
    return return_200_wrapper()
