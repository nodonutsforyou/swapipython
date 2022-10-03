import pytest
import requests
import logging
import json

log = logging.getLogger("test_all_endpoints")

def generate_list_of_all_endpoints():
    list = [("https://swapi.dev/api/", 200)]
    endpoint = "https://swapi.dev/api/"
    r = requests.get(endpoint)
    assert r.status_code == 200, f'endpoint {endpoint} does not return expected error code ({r.status_code} != 200'
    endpoints = json.loads(r.text)
    assert len(endpoints) > 0, f'endpoint {endpoint} does not contain expected list of endpoints'
    for key, value in endpoints.items():
        endpoint_to_call = (value, 200)
        endpoint_with_schema = (value + "schema/", 200)
        r = requests.get(value)
        if r.status_code == 200:
            item = json.loads(r.text)
            endpoint_with_number = (item["results"][0]["url"], 200)
        else:
            endpoint_with_number = (value + "1/", 404)
        list.append(endpoint_to_call)
        list.append(endpoint_with_number)
        list.append(endpoint_with_schema)
    return list


LIST_OF_ENDPOINTS = generate_list_of_all_endpoints()



""""
test suite that hits all the possible endpoints.
"""
@pytest.mark.parametrize("endpoint,expected_status", LIST_OF_ENDPOINTS)
def test_all_endpoints(endpoint, expected_status):
    r = requests.get(endpoint)
    log.info("GET %s: %s", endpoint, r.text)
    assert r.status_code == expected_status, f'endpoint {endpoint} does not return expected error code ({r.status_code} != {expected_status}'
