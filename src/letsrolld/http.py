import json
import logging
from http.client import HTTPConnection

import requests


# TODO: use a library to fill these in
_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.39.0",
}


# stolen from stackoverflow
def enable_debug():
    """Switches on logging of the requests module."""
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def get_url(url):
    return requests.get(url, timeout=120).text


def get_json(url, data):
    return json.loads(requests.post(url, headers=_HEADERS, json=data).text)
