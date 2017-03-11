# -*- coding: utf-8 -*-
from copy import deepcopy


def block_message(button_block_name, hotel):
    element_base = {
        "title": hotel['title'],
        "image_url": "",
        "subtitle": hotel['subtitle'],
        "buttons": [
            {
                "type": "web_url",
                "url": hotel['hotel_url'][0],
                "title": "飯店介紹"
            }
        ]
    }
    elements = []
    for i in hotel['image_urls']:
        copied_element = deepcopy(element_base)
        copied_element["image_url"] = i
        elements.append(copied_element)

    result = {
        "messages": [
            {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements
                    }
                }
            }
        ]
    }
    return result
