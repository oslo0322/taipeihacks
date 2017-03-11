# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import random

import logging

import fetch_by_v2_api as fbs
import fb_template as ft


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

        user_text = request.args.get('user_text', None)
        self.offset = 0

        self.nlp_text = self.apply_nlp(user_text)
        self._setter()

    def apply_nlp(self, user_text):
        return user_text

    def _setter(self):
        if not self.nlp_text:
            return

        if self.nlp_text == "cheaper":
            self.price = self.price * 0.9
            return

        if self.nlp_text == "reset":
            self.price = 100
            self.stars = 3
            self.review_scores = 7
            self.place = self.ref_place
            return

        if len(self.nlp_text) > 3:
            self.place = self.nlp_text
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
