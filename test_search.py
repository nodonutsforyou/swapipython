import logging
import json
import urllib.parse
import pytest
import requests

log = logging.getLogger("test_search")


@pytest.mark.parametrize("name", [
    "Luke Skywalker",
])
def test_positive_type(name):
    """
    A test that find All Details about the home world, films, vehicles, and starships for Luke
    Skywalker assuming you only know the name “Luke Skywalker”.
    """
    endpoint = "https://swapi.dev/api/people/?search=" + str(urllib.parse.quote(name))
    r = requests.get(endpoint)
    # checks if call returning expected status call
    assert r.status_code == 200, f'endpoint {endpoint} does not return expected error code ({r.status_code})'
    results = json.loads(r.text)
    assert results["count"] == 1, f'found {results["count"]} items {name}'
    data = results["results"][0]
    # home world
    homeworld_reply = requests.get(data["homeworld"])
    assert homeworld_reply.status_code == 200, f'endpoint {data["homeworld"]} does not return expected error code ({homeworld_reply.status_code})'
    log.info(homeworld_reply.text)
    # films
    for film in data["films"]:
        film_reply = requests.get(film)
        assert film_reply.status_code == 200, f'endpoint {film} does not return expected error code ({film_reply.status_code})'
        log.info(film_reply.text)
    # vehicles
    for vehicle in data["vehicles"]:
        vehicle_reply = requests.get(vehicle)
        assert vehicle_reply.status_code == 200, f'endpoint {vehicle} does not return expected error code ({vehicle_reply.status_code})'
        log.info(vehicle_reply.text)
    # starships
    for starship in data["starships"]:
        starship_reply = requests.get(starship)
        assert starship_reply.status_code == 200, f'endpoint {starship} does not return expected error code ({starship_reply.status_code})'
        log.info(starship_reply.text)
