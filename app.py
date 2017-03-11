# -*- coding: utf-8 -*-

import os
import sys
import requests
import urllib
import json
import tempfile

from urllib import quote
from argparse import ArgumentParser
from flask import json
from flask import Flask, request, abort

app = Flask(__name__)


# BASE_DIR = './'
# static_tmp_path = os.path.join(BASE_DIR, 'ven')
# handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@app.route("/api/v1/ok")
def ok():
    ok = app.response_class(
        response=json.dumps({ 'status' : 'ok','text':"123",'timestamp':12345}),
        status=200,
        mimetype='application/json'
    )
    return ok


if __name__ == "__main__":

    # 暫存檔位置 若無就打開
    # path = BASE_DIR + "/static/tmp"
    # if not os.path.isdir(path):
    #     os.mkdir(BASE_DIR + "/static")
    #     os.mkdir(BASE_DIR + "/static/tmp")

    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
