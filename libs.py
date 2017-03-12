# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import random

import logging
import re

import fetch_by_v2_api as fbs
import fb_template as ft
from fetching_booking_api import get_nlp_result, get_google_nearby


def get_args(request):
    price = request.get('price')
    stars = request.get('stars')
    review_scores = request.get('review_scores')
    pos = request.get('pos')
    return int(float(price)), int(float(stars)), int(float(review_scores)), pos


class RequestHelper(object):

    def __init__(self, request):
        self.ref = request.args.get('ref')
        self.start, self.end, self.ref_place, self.people = self.ref.split(",")
        self.price, self.stars, self.review_scores, self.pos = get_args(request.args)

        self.place = request.args.get('place', None) or self.ref_place

        self.user_text = request.args.get('user_text', None)
        self.offset = 0
        self.recommend = False
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
                        self.price *= random.uniform(1.5, 2.5)
                    else:
                        self.price *= random.uniform(1.1, 1.8)
                else:
                    self.price *= random.uniform(0.6, 0.99)

            if i == "stars":
                self._modifier(i, (1, 5), _status)

            if i == "review_scores":
                self._modifier(i, (1, 10), _status)

    def _setter(self):
        if not self.user_text:
            return

        suggest_keywords = ["suggest", "recommend", "around"]
        for s in suggest_keywords:
            if re.search(s, self.user_text):
                self.recommend = True
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
        return fbs.main(self.place, self.start, self.end, self.people,
                        stars=self.stars,
                        offset=self.offset,
                        min_review_score=self.review_scores,
                        min_price=self.price)

    @classmethod
    def error_message(cls):
        return ft.empty_message()

    def _get_hotel_message(self):
        try:
            hotel = self.hotel_from_messengers
            self.pos = hotel.pop("pos")
            return ft.block_message(hotel, self.get_attrs)
        except Exception as e:
            logging.error(e, exc_info=True)
            return self.error_message()

    def _get_recommend_message(self):
        nearby = get_google_nearby(self.pos)
        text = "\n".join(nearby)
        return ft.recommend_message(text)

    def get_message(self):
        if self.recommend:
            return self._get_recommend_message()
        return self._get_hotel_message()

    @property
    def get_attrs(self):
        return {
            "price": int(self.price),
            "stars": int(self.stars),
            "review_scores": int(self.review_scores),
            "place": self.place,
            "pos": self.pos
        }
