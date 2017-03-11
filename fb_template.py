# -*- coding: utf-8 -*-

def block_message(button_block_name, hotel):
    messages = []
    messages.append({"text": "以下房型推薦給你～"})
    messages.append({
          "attachment": {
              "type": "template",
              "payload": {
                  "template_type": "generic",
                  "elements": [
                      {
                          "title": hotel['title'],
                          "image_url": hotel['image_urls'][0],
                          "subtitle": hotel['subtitle'],
                          "buttons": [
                              {
                                  "type": "web_url",
                                  "url": hotel['hotel_url'][0],
                                  "title": "飯店介紹"
                              }
                          ]
                      }
                  ]
              }
          }
      })
    messages.append({
          "attachment": {
              "type": "template",
              "payload": {
                  "template_type": "generic",
                  "elements": [
                      {
                          "title": hotel['title'],
                          "image_url": hotel['image_urls'][1],
                          "subtitle": hotel['subtitle'],
                          "buttons": [
                              {
                                  "type": "web_url",
                                  "url": hotel['hotel_url'][0],
                                  "title": "飯店介紹"
                              }
                          ]
                      }
                  ]
              }
          }
      })
    messages.append({
          "attachment": {
              "type": "template",
              "payload": {
                  "template_type": "generic",
                  "elements": [
                      {
                          "title": hotel['title'],
                          "image_url": hotel['image_urls'][2],
                          "subtitle": hotel['subtitle'],
                          "buttons": [
                              {
                                  "type": "web_url",
                                  "url": hotel['hotel_url'][0],
                                  "title": "飯店介紹"
                              }
                          ]
                      }
                  ]
              }
          }
      })
    return {
  "messages":[
    {
      "attachment":{
        "type":"template",
        "payload":{
          "template_type":"generic",
          "elements":[
            {
              "title":hotel['title'],
              "image_url":hotel['image_urls'][0],
              "subtitle":hotel['subtitle'],
              "buttons":[
                  {
                      "type": "web_url",
                      "url": hotel['hotel_url'][0],
                      "title": "飯店介紹"
                  }
              ]
            },
            {
              "title":hotel['title'],
              "image_url":hotel['image_urls'][1],
              "subtitle":hotel['subtitle'],
              "buttons":[
                {
                      "type": "web_url",
                      "url": hotel['hotel_url'][0],
                      "title": "飯店介紹"
                }
              ]
            },
              {
                  "title": hotel['title'],
                  "image_url": hotel['image_urls'][2],
                  "subtitle": hotel['subtitle'],
                  "buttons": [
                      {
                          "type": "web_url",
                          "url": hotel['hotel_url'][0],
                          "title": "飯店介紹"
                      }
                  ]
              }
          ]
        }
      }
    }
  ]
}
