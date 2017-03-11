# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
from argparse import ArgumentParser

from flask import Flask
from flask import json
from flask import request

from libs import RequestHelper

app = Flask(__name__)


@app.route("/api/v1/choose")
def choose():
    message = RequestHelper(request).get_message()

    return app.response_class(
        response=json.dumps(message),
        status=200,
        mimetype='application/json'
    )


@app.route("/api/v1/welcome")
def welcome():
    message = RequestHelper(request).get_message()

    return app.response_class(
        response=json.dumps(message),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
