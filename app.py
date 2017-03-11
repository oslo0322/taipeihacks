# -*- coding: utf-8 -*-

import json
import fb_template as ft
import fetch_by_v2_api as fbs
from argparse import ArgumentParser

from flask import Flask
from flask import json
from flask import request

app = Flask(__name__)


def get_args(request):
    price = request.get('price')
    stars = request.get('stars')
    review_scores = request.get('review_scores')
    return int(float(price)), int(float(stars)), int(float(review_scores))


@app.route("/api/v1/choose")
def choose():
    ref = request.args.get('ref')
    start, end, place = ref.split(",")
    choose = request.args.get('user_text')

    price, stars, review_scores = get_args(request.args)

    if choose == "cheaper":
        price = price*0.9
        set_attrs = {
           "price": int(price),
           "stars": int(stars),
           "review_scores": int(review_scores),
        }
    elif choose == "reset":
        set_attrs = {
           "price": 100,
           "stars": 3,
           "review_scores": 7,
        }
    else:
        set_attrs = None

    hotel = fbs.main(place, start, end, stars=stars,
                     min_review_score=review_scores, min_price=price)
    ok = app.response_class(
        response=json.dumps(ft.block_message('bargain', hotel, set_attrs=set_attrs)),
        status=200,
        mimetype='application/json'
    )
    return ok


@app.route("/api/v1/welcome")
def ok():
    ref = request.args.get('ref')
    start, end, place = ref.split(",")

    price, stars, review_scores = get_args(request.args)

    hotel = fbs.main(place, start, end, stars=stars,
                     min_review_score=review_scores, min_price=price)

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
