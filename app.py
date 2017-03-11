# -*- coding: utf-8 -*-

import json
from argparse import ArgumentParser

from flask import Flask
from flask import json

app = Flask(__name__)


@app.route("/api/v1/ok")
def ok():
    ok = app.response_class(
        response=json.dumps({'status': 'ok', 'text': "123", 'timestamp': 12345}),
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
