import pytest
import requests
import logging
import json
import re
import sys

log = logging.getLogger("test_people")


"""
Documentation on website https://swapi.dev/documentation#people clearly states, that there should be a /schema/ call.
I thought there should be a nice way to get a json schema call, so i could test every single reply with provided schema. But somehow all the /schema/ endpoint returning 404 codes.
I've tried to find references to this call in provided CLI, but they have no references to it whatsoever. I assume this is a bug, so I'm living a failed test here
"""
def test_people_endpoint_schema():
    endpoint = "https://swapi.dev/api/people/schema/"
    r = requests.get(endpoint)
    log.info("GET %s: %s", endpoint, r.text)
    assert r.status_code == 200

def get_page_number(url: str):
    a = re.search(r"https:\/\/swapi.dev\/api\/people\/\?page=([0-9]]*)$", url)
    if a:
        return int(a.group(1))
    return None

"""
simple positive test to check the types of all the fields of an item
"""
@pytest.mark.parametrize("id", [
    1,
    32,
])
def test_positive_type(id):
    endpoint = "https://swapi.dev/api/people/" + str(id)
    r = requests.get(endpoint)
    # checks if call returning expected status call
    assert r.status_code == 200, f'endpoint {endpoint} does not return expected error code ({r.status_code})'
    person = json.loads(r.text)

    expected_string_fields = [
        "name",
        "birth_year",
        "eye_color",
        "gender",
        "hair_color",
        "height",
        "height",
        "mass",
        "skin_color",
        "homeworld",
        "url",
        "created",
        "edited",
    ]
    expected_list_fields = [
        "films",
        "species",
        "starships",
        "vehicles",
    ]
    for string_field in expected_string_fields:
        assert string_field in person, f'json does not contain expected field {string_field}:\n{str(person)}'
        assert type(person[string_field]) is str, f'json does not have expected type for a field {string_field}:\n{str(person)}'
    for list_field in expected_list_fields:
        assert list_field in person, f'json does not contain expected field {string_field}:\n{str(person)}'
        assert type(person[list_field]) is list, f'json does not have expected type for a field {string_field}:\n{str(person)}'


"""
test pagination of the endpoint
"""
def test_paginations():
    endpoint = "https://swapi.dev/api/people/"
    # initial call
    r = requests.get(endpoint)
    # checks if call returning expected status call
    assert r.status_code == 200, f'endpoint {endpoint} does not return expected error code ({r.status_code})'
    people = json.loads(r.text)
    size = people["count"]
    next_page = people["next"]
    previous_page = people["previous"]
    # checks if there is correct total size count
    assert type(size) == int, f'Incorrect value in count field ({str(size)})'
    # check if DB is not empty
    assert size > 0, f'Incorrect value in count field ({str(size)})'
    # checks if previous_page is empty
    assert previous_page is None, f'Incorrect pagination on page 1. Expected: no previous page, Actual: ({people["previous"]})'
    # checks if next_page is page number 2
    assert next_page == endpoint + "?page=2", f'Incorrect pagination on page 1. Expected: link to page 2, Actual: ({people["next"]})'
    collected_items = len(people["results"])
    page_number = 2
    # loop through all the pages
    while collected_items < size:
        this_page = next_page
        r = requests.get(next_page)
        # check status_code
        assert r.status_code == 200, f'endpoint {next_page} does not return expected error code ({r.status_code})'
        page_results = json.loads(r.text)
        page_len = len(page_results["results"])
        # we expect no empty pages
        assert page_len > 0, f'page {page_number} is empty (GET {this_page})'
        previous_page = page_results["previous"]
        next_page = page_results["next"]
        collected_items += page_len
        # we expect page numbers to be ordered correctly and have well formated urls
        assert page_number-1 == get_page_number(previous_page), f'Unexpected previous page link: {previous_page}'
        if collected_items < size:
            assert page_number+1 == get_page_number(next_page), f'Unexpected next page link: {next_page}'
        page_number += 1
    # checks specific for the last page
    assert next_page is None, f'Incorrect pagination on page 1. Expected: no next page, Actual: ({next_page})'
    assert collected_items == size, f'Unexpected number of collected items across all pages'
    # check that page larger than max returns error
    non_exisitng_page_url = endpoint+"?page="+str(page_number)
    r = requests.get(non_exisitng_page_url)
    assert r.status_code == 404, f'endpoint {non_exisitng_page_url} does not return expected error code ({r.status_code})'


"""
list of negative tests - list of possible wrong urls to check
"""
@pytest.mark.parametrize("endpoint,expected_code,expected_text", [
    ("https://swapi.dev/api/people/?page=0", 404, "Not found"),
    ("https://swapi.dev/api/people/?page=-1", 404, "Not found"),
    ("https://swapi.dev/api/people/?page=nan", 404, "Not found"),
    ("https://swapi.dev/api/people/?page=1" + str(sys.maxsize), 404, "Not found"),
    ("https://swapi.dev/api/people/?page=1.1", 404, "Not found"),
    ("https://swapi.dev/api/people/0", 404, "Not found"),
    ("https://swapi.dev/api/people/99", 404, "Not found"),
    ("https://swapi.dev/api/people/-1", 404, "Not found"),
    ("https://swapi.dev/api/people/nan", 404, "Not found"),
    ("https://swapi.dev/api/people/luke", 404, "Not found"),
    ("https://swapi.dev/api/people/1" + str(sys.maxsize), 404, "Not found"),
    ("https://swapi.dev/api/people/1.1", 404, "Not found"),
])
def test_wrong_urls(endpoint, expected_code, expected_text):
    r = requests.get(endpoint)
    # checks if call returning expected status call
    assert r.status_code == expected_code, f'endpoint {endpoint} does not return expected error code ({r.status_code} != {expected_code}'
    assert expected_text.lower() in r.text.lower()


"""
test to do the following:
• fails if the person has no hair color (i.e. hair color is n/a)
• fails if a person has no gender (i.e. gender is unknown or n/a)
• fails if the person has not piloted a vehicle
"""
@pytest.mark.parametrize("id", [
    1,
    32,
    8,
    6,
    15,
])
def test_hair_color_gender_vehicles(id):
    endpoint = "https://swapi.dev/api/people/" + str(id)
    r = requests.get(endpoint)
    # checks if call returning expected status call
    assert r.status_code == 200, f'endpoint {endpoint} does not return expected error code ({r.status_code})'
    person = json.loads(r.text)
    # get list of all the erros, so we can return list, but not failed on first failed condition
    errors = ""
    if person["hair_color"] == "n/a":
        errors += f'{person["name"]}(id:{id}) has hair color {person["hair_color"]}\n'
    if person["gender"] == "n/a":
        errors += f'{person["name"]}(id:{id}) has gender {person["hair_color"]}\n'
    if len(person["vehicles"]) == 0:
        errors += f'{person["name"]}(id:{id}) has no vehicles assigned\n'
    assert errors == "", errors

