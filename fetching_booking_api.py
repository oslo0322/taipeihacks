import json

import requests
from requests.auth import HTTPBasicAuth

endpoint = "https://distribution-xml.booking.com/json"

def get_booking_api_response(uri, payload):
    url = endpoint + uri
    result = requests.get(url, params=payload, auth=HTTPBasicAuth('hacker234', '8hqNW6HtfU'))
    return json.loads(result.content)

