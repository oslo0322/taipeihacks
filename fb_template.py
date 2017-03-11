# -*- coding: utf-8 -*-

def block_message(button_block_name, image_url):
    return {
  "messages":[
      {"text": "以下房型推薦給你～"},
      {
          "attachment": {
              "type": "template",
              "payload": {
                  "template_type": "generic",
                  "elements": [
                      {
                          "title": "IBIS",
                          "image_url": image_url,
                          "subtitle": "總統套房",
                          "buttons": [
                              {
                                  "type": "show_block",
                                  "block_name": button_block_name,
                                  "title": "議價"
                              }
                          ]
                      }
                  ]
              }
          }
      }
  ]
}
