import requests
from places_coord.models import Place
from environs import Env
from django.utils import timezone


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
        env = Env()
        env.read_env()
        place.lat, place.lon = fetch_coordinates(env('YANDEX_TOKEN'), address)
        if place.lat and place.lon:
            place.save()
            return place.lat, place.lon
        else:
            place.lat = place.lon = None
            place.update_at = timezone.now()
            place.save()
            return place.lat, place.lon
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        place.lat = place.lon = None
        place.update_at = timezone.now()
        place.save()
        return place.lat, place.lon

