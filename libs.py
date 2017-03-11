# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import random

import logging

import fetch_by_v2_api as fbs
import fb_template as ft
from fetching_booking_api import get_nlp_result


def get_args(request):
    price = request.get('price')
    stars = request.get('stars')
    review_scores = request.get('review_scores')
    return int(float(price)), int(float(stars)), int(float(review_scores))


class RequestHelper(object):

    def __init__(self, request):
        self.ref = request.args.get('ref')
        self.start, self.end, self.ref_place, self.people = self.ref.split(",")
        self.price, self.stars, self.review_scores = get_args(request.args)

        self.place = request.args.get('place', None) or self.ref_place

        self.user_text = request.args.get('user_text', None)
        self.offset = 0

        self._setter()

    def _modifier(self, name, limit, status):
        attr = getattr(self, name)
        min, max = limit[0], limit[1]
        if status == "up":
            setattr(self, name, attr+1)
        else:
            setattr(self, name, attr-1)

        if attr > max:
            setattr(self, name, max)

        if attr < min:
            setattr(self, name, min)

    def apply_nlp(self, nlp_result):
        _types, _status = nlp_result
        types = {
            "price": ["price"],
            "star": ["stars"],
            "review": ["review_scores"],
            "all": ["price", "stars", "review_scores"]
        }

        for i in types[_types]:
            if i == "price":
                if _status == "up":
                    if _types == "all":
                        self.price *= random.uniform(2.1, 5.0)
                    else:
                        self.price *= random.uniform(1.1, 3.0)
                else:
                    self.price *= random.uniform(0.6, 0.99)

            if i == "stars":
                self._modifier(i, (1, 5), _status)

            if i == "review_scores":
                self._modifier(i, (1, 10), _status)

    def _setter(self):
        if not self.user_text:
            return

        nlp_result = get_nlp_result(self.user_text)
        if nlp_result:
            self.apply_nlp(nlp_result)
            self.offset = random.randint(1, 10)
            return

        if self.user_text == "reset":
            self.price = 100
            self.stars = 3
            self.review_scores = 7
            self.place = self.ref_place
            return

        if len(self.user_text) > 3:
            self.place = self.user_text
            self.offset = random.randint(1, 100)
            return

    @property
    def hotel_from_messengers(self):
        print(self.place)
        return fbs.main(self.place, self.start, self.end, self.people,
                        stars=self.stars,
                        offset=self.offset,
                        min_review_score=self.review_scores,
                        min_price=self.price)

    @classmethod
    def error_message(cls):
        return ft.empty_message()

    def get_message(self):
        try:
            hotel = self.hotel_from_messengers
            return ft.block_message(hotel, self.get_attrs)
        except Exception as e:
            logging.error(e, exc_info=True)
            return self.error_message()

    @property
    def get_attrs(self):
        return {
            "price": int(self.price),
            "stars": int(self.stars),
            "review_scores": int(self.review_scores),
            "place": self.place
        }
