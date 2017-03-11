# -*- coding: utf-8 -*-

def block_message(button_block_name, image_url):
    messages = []
    messages.append({"text": "以下房型推薦給你～"})
    messages.append(      {
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
      })
    return {
  "messages":messages
}
