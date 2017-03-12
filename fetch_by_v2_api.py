# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import logging

from fetch_by_search import get_hotels_url_by_id, get_hotels_photo
from fetching_booking_api import get_booking_api_response, get_google_nearby


def get_data_from_auto_complete(text, lang="en"):
    payload = {'languagecode': lang, "text": text}
    uri = "/bookings.autocomplete"
    data = get_booking_api_response(uri, payload)
    get_cities_id_list = []
    for i in data:
        if "longitude" not in i or "latitude" not in i:
            continue
        get_cities_id_list.append({
            "longitude": i["longitude"],
            "latitude": i["latitude"],
        })
    return get_cities_id_list[0]


def _app_map_info(pos):
    url = ("https://maps.googleapis.com/maps/api/staticmap?"
           "zoom=18&size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C"
           + pos["latitude"] + "," + pos["longitude"] +
           "&key="+os.environ["GOOGLE_API_KEY"])
    return url


def main(place, checkin, checkout, people, stars=1, offset=0, min_review_score=1, min_price=50, max_price=2000):
    pos = get_data_from_auto_complete(place)
    payload = {
        "checkin": checkin,
        "checkout": checkout,
        "longitude": pos["longitude"],
        "latitude": pos["latitude"],
        "room1": ",".join(["A"]*int(people)),
        "min_price": int(min_price),
        "max_price": int(max_price),
        "output": "hotel_details",
        "rows": 1,
        "stars": stars,
        "min_review_score": min_review_score,
        "radius": 50,
        "order_by": "price",
        "currency_code": "USD",
        "offset": offset
    }
    uri = "/getHotelAvailabilityV2"
    data = get_booking_api_response(uri, payload)
    if not data:
        return None
    try:
        logging.info(data["hotels"][0])
    except Exception:
        logging.error(data)
    hotel_id = data["hotels"][0]["hotel_id"]
    price = data["hotels"][0]["price"]
    hotel_name = data["hotels"][0]["hotel_name"]
    review_score = data["hotels"][0]["review_score"]
    photos = [_app_map_info(pos), get_hotels_photo(hotel_id)[0],
              get_hotels_photo(hotel_id)[1], get_hotels_photo(hotel_id)[2]]
    url = get_hotels_url_by_id(hotel_id)

    return {
        "title": hotel_name,
        "subtitle": "Review: {review_score}, Price: {price}".format(review_score=review_score,
                                                                          price=price),
        "image_urls": photos,
        "hotel_url": url,
        "hotel_id": hotel_id,
        "pos": ",".join([pos["latitude"], pos["longitude"]]),
    }
