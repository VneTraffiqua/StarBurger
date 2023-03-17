import requests
from places.models import Place
from environs import Env
from django.utils import timezone
from star_burger.settings import YANDEX_TOKEN


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def add_place(address):
    place, _ = Place.objects.get_or_create(address=address)
    try:
        place.lat, place.lon = fetch_coordinates(YANDEX_TOKEN, address)
        if place.lat and place.lon:
            place.save()
            return place.lat, place.lon
        else:
            return RuntimeError
    except (
            requests.exceptions.RequestException,
            requests.exceptions.HTTPError,
            RuntimeError
    ):
        place.lat = place.lon = None
        place.update_at = timezone.now()
        place.save()
        return place.lat, place.lon

