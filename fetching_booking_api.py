import json
import re

import requests
from requests.auth import HTTPBasicAuth

endpoint = "https://distribution-xml.booking.com/json"


def get_booking_api_response(uri, payload):
    url = endpoint + uri
    result = requests.get(url, params=payload, auth=HTTPBasicAuth('hacker234', '8hqNW6HtfU'))
    return json.loads(result.content)


def get_nlp_result(query_string):

    def _get_status(_intent):
        keywords = {
            "up": ["up", "increase"],
            "down": ["under", "decrease"]
        }
        for key, value in keywords.items():
            for _v in value:
                if _v in _intent:
                    return key

    def _in_up_keywords(string):
        up_keywords = ["luxury", "affluence", "comfort", "enjoy", "extravagance", "leisure", "rich", "opulence"]
        for i in up_keywords:
            if re.search(i, string):
                return True
        return False

    def _intent_parser(intent):
        split_intent = intent.split("_")
        types = ["star", "review", "price"]
        for _type in types:
            if _type in split_intent:
                result = _get_status(split_intent)
                if result:
                    return _type, result
                return None

    if _in_up_keywords(query_string):
        return "all", "up"

    endpoint = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/d2d3350e-e867-4a73-9a51-81a0bd96e6a3"
    payload = {
        "subscription-key": "0c837e0f69604166b9c07627bfc7011e",
        "verbose": "true",
        "q": query_string
    }
    result = requests.get(endpoint, params=payload)
    data = json.loads(result.content)
    if data["topScoringIntent"]["score"] > 0.5:
        intent = data["topScoringIntent"]["intent"]
        return _intent_parser(intent)
