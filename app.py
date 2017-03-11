# -*- coding: utf-8 -*-

import json
import fb_image
import fb_template as ft
import fetch_by_v2_api as fbs
import fb_text_message as ftm
import requests
from argparse import ArgumentParser

from flask import Flask
from flask import json
from flask import request

app = Flask(__name__)


@app.route("/api/v1/ok")
def ok():
    user_text = request.args.get('user_text')
    print user_text
    hotel = fbs.main("Tokyo", "2017-06-02", "2017-06-03", stars=3, min_review_score=8, min_price=100)
    ok = app.response_class(
        response=json.dumps(ft.block_message('bargain', hotel)),
        status=200,
        mimetype='application/json'
    )
    return ok


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
