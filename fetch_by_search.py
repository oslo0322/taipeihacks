from collections import OrderedDict
from datetime import datetime, timedelta

from fetching_booking_api import get_booking_api_response


def get_data_from_auto_complete(text, lang="en"):
    payload = {'languagecode': lang, "text": text}
    uri = "/bookings.autocomplete"
    data = get_booking_api_response(uri, payload)
    get_cities_id_list = set()
    for i in data:
        if i["city_ufi"]:
            get_cities_id_list.add(i["city_ufi"])

    return list(get_cities_id_list)


def get_data_from_hotels(cities, limits=3, lang="en"):
    payload = {'languagecode': lang, "rows":limits, "city_ids": ",".join(cities)}

    uri = "/bookings.getHotels"
    data = get_booking_api_response(uri, payload)
    get_hotels_id = []
    for i in data:
        get_hotels_id.append(i["hotel_id"])

    return get_hotels_id


def get_hotels_url_by_id(hotel_ids, lang="en"):
    payload = {'languagecode': lang, "hotel_ids": hotel_ids}
    uri = "/bookings.getHotels"
    data = get_booking_api_response(uri, payload)
    return [i["url"] for i in data]


def get_hotels_photo(hotel):
    payload = {"hotel_ids": hotel}
    uri = "/bookings.getHotelDescriptionPhotos"
    data = get_booking_api_response(uri, payload)
    return [i["url_original"] for i in data]


def get_hotels(hotels, arrival_date, departure_date):
    uri = "/bookings.getBlockAvailability"
    payload = {'arrival_date': arrival_date,
               "departure_date":departure_date,
               "hotel_ids": ",".join(hotels)}
    data = get_booking_api_response(uri, payload)
    result = []
    for i in data:
        hotel_id = i["hotel_id"]
        currency = ""
        min_prices = []
        for b in i["block"]:
            min_prices.append(b["min_price"]["price"])
            currency = b["min_price"]["currency"]

        result.append({
            "hotel_id": hotel_id,
            "currency": currency,
            "min_price": sorted(min_prices)[0]  # lowest price
        })

    return result

def main(place, arrival_date_str):
    arrival_date = datetime.strptime(arrival_date_str, "%Y-%m-%d")
    departure_date = arrival_date + timedelta(days=1)
    cities = get_data_from_auto_complete(place)
    hotels = get_data_from_hotels(cities)

    hotels_data = get_hotels(hotels, arrival_date.date().isoformat(), departure_date.date().isoformat())

    photos = get_hotels_photo(hotels_data[0]["hotel_id"])
    print(hotels_data[0]["hotel_id"])
    return photos


if __name__ == '__main__':
    print list(main("Tokyo", "2017-04-01"))
