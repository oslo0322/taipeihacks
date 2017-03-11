# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from fetch_by_search import get_hotels_url_by_id, get_hotels_photo
from fetching_booking_api import get_booking_api_response


def get_data_from_auto_complete(text, lang="en"):
    payload = {'languagecode': lang, "text": text}
    uri = "/bookings.autocomplete"
    print(payload)
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


def main(place, checkin, checkout, stars=1, offset=0, min_review_score=1, min_price=50, max_price=2000):
    pos = get_data_from_auto_complete(place)
    payload = {
        "checkin": checkin,
        "checkout": checkout,
        "longitude": pos["longitude"],
        "latitude": pos["latitude"],
        "room1": "A,A",
        "min_price": int(min_price),
        "max_price": int(max_price),
        "output": "hotel_details",
        "rows": 1,
        "stars": stars,
        "min_review_score": min_review_score,
        "radius": 50,
        "order_by": "price",
        "currency_code": "TWD",
        "offset": offset
    }
    uri = "/getHotelAvailabilityV2"
    data = get_booking_api_response(uri, payload)
    if not data:
        return None
    hotel_id = data["hotels"][0]["hotel_id"]
    price = data["hotels"][0]["price"]
    hotel_name = data["hotels"][0]["hotel_name"]
    review_score = data["hotels"][0]["review_score"]
    photos = [get_hotels_photo(hotel_id)[0], get_hotels_photo(hotel_id)[1], get_hotels_photo(hotel_id)[2]]
    url = get_hotels_url_by_id(hotel_id)
    return {
        "title": hotel_name,
        "subtitle": "review_score: {review_score}, price: {price}".format(review_score=review_score,
                                                                          price=price),
        "image_urls": photos,
        "hotel_url": url,
        "hotel_id": hotel_id
    }


if __name__ == '__main__':
    print(main("Tokyo", "2017-06-02", "2017-06-10", min_price=10))
    print(main("Tokyo", "2017-06-02", "2017-06-10", min_price=40))
