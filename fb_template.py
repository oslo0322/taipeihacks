# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy


def empty_message():
    result = {
        "messages": [
            {"text": "Sorry, Hotels not found, please use other key words try again!!"},
        ]
    }
    return result


def recommend_message(text):
    result = {
        "messages": [
            {"text": text},
        ]
    }
    return result


def block_message(hotel, set_attrs=None):
    element_base = {
        "title": hotel['title'],
        "image_url": "",
        "subtitle": hotel['subtitle'],
        "buttons": [
            {
                "type": "web_url",
                "url": hotel['hotel_url'][0],
                "title": "Booking Now!"
            }
        ]
    }
    elements = []
    for i in hotel['image_urls']:
        copied_element = deepcopy(element_base)
        copied_element["image_url"] = i
        elements.append(copied_element)

    reply_titles = ["Cheaper option", "Better review", "More stars", "Luxury hotel!", "reset"]
    replies = []
    for reply in reply_titles:
        replies.append({
            "title": reply,
            "block_names": ["Default answer"]
        })

    result = {
        "messages": [
            {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements
                    }
                }, "quick_replies": replies
            }
        ]
    }

    if set_attrs:
        set_result = {key: value for key, value in set_attrs.items()}
        result.update({
            "set_attributes": set_result
        })

    return result
