# -*- coding: utf-8 -*-

def block_message(button_block_name, hotels):
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
                          "image_url": "http://aff.bstatic.com/images/hotel/max500_watermarked_standard/875/8759de7ffd6f346f75a3eb8ddc1ff2c2971403eb.jpg",
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
