"""unit tests for residnce module"""

import requests

from flat_search.residence import (
    ResidentFilter,
    get_bathroom_count,
    get_bedroom_count,
    get_id,
    get_price,
    get_published_date,
    get_residences,
    get_size,
    get_url_path,
)
from tests.unit.helper import get_mock_response


def test_get_bathroom():
    """happy path test - retrieve bathrooms from the resident object"""

    residence = {"bathrooms": 2}

    expected_result = 2
    actual_result = get_bathroom_count(residence)

    assert expected_result == actual_result


def test_get_bedrooms():
    """happy path test - retrieve bedrooms from the resident object"""

    residence = {"bedrooms": 3}

    expected_result = 3
    actual_result = get_bedroom_count(residence)

    assert expected_result == actual_result


def test_get_price():
    """happy path test - retrieve price from the resident object"""

    residence = {"price": {"amount": 475000, "currencyCode": "GBP"}}

    expected_result = ("GBP", 475000)
    actual_result = get_price(residence)

    assert expected_result == actual_result


def test_get_published_date():
    """happy path test - retrieve date resident first appeared on the site"""

    residence = {"firstVisibleDate": "2025-01-13T15:41:06Z"}

    expected_result = "2025-01-13T15:41:06Z"
    actual_result = get_published_date(residence)

    assert expected_result == actual_result


def test_get_size():
    """happy path test - retrieve size from the resident object"""

    residence = {"displaySize": "814 sq. ft."}

    expected_result = ("sq. ft.", 814)
    actual_result = get_size(residence)

    assert expected_result == actual_result


def test_get_size_with_comma():
    """retrieve size from the resident object where , thousand delimiter is used"""

    residence = {"displaySize": "1,234 sq. ft."}

    expected_result = ("sq. ft.", 1234)
    actual_result = get_size(residence)

    assert expected_result == actual_result


def test_get_size_not_present():
    """unhappy path test - retreive price from the resident object when not present"""

    residence = {"displaySize": ""}

    expected_result = (None, None)
    actual_result = get_size(residence)

    assert expected_result == actual_result


def test_get_id():
    """happy path test - retreive id from the resident object"""

    residence = {"id": 12345}

    expected_result = 12345
    actual_result = get_id(residence)

    assert expected_result == actual_result


def test_get_url_path():
    """happy path test - retreive address from the resident object"""

    residence = {"propertyUrl": "/properties/147763901#/?channel=RES_BUY"}

    expected_result = "/properties/147763901#/?channel=RES_BUY"
    actual_result = get_url_path(residence)

    assert expected_result == actual_result


def test_get_reseidences(monkeypatch, right_move_page):
    """happy path test - get residences from a rightmove html page"""

    residences = [
        147763901,
        139112297,
        152984657,
        152983178,
        156816329,
        156514496,
        156245768,
        148220504,
        154183337,
        150174641,
        107278337,
        150996110,
        147763901,
        156946703,
        87039912,
        156675053,
        156871805,
        154176836,
        147282281,
        156326468,
    ]

    with monkeypatch.context() as m:
        m.setattr(requests, "get", get_mock_response(right_move_page))

        expected_result = residences
        actual_result = [residence["id"] for residence in get_residences()]

    assert expected_result == actual_result


def test_get_resedences_with_filter(monkeypatch, right_move_page):
    """happy path test - get residences from a rightmove html page with a filter"""

    residences = [
        147763901,
        139112297,
        152984657,
        152983178,
        156816329,
        156514496,
        156245768,
        148220504,
        154183337,
        150174641,
        107278337,
        150996110,
        147763901,
        156946703,
        87039912,
        156675053,
        156871805,
        154176836,
        147282281,
        156326468,
    ]

    search_filter = ResidentFilter(
        locationIdentifier="POSTCODE^623999",
        min_bedrooms=2,
        min_price=0,
        residence_type="flat",
        radius=0.25,
        min_bathrooms=0,
        min_size=0,
    )

    with monkeypatch.context() as m:
        m.setattr(requests, "get", get_mock_response(right_move_page))

        expected_result = residences
        actual_result = [
            residence["id"]
            for residence in get_residences(residence_filter=search_filter)
        ]

    assert expected_result == actual_result
