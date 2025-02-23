"""unit tests for residnce module"""

import requests

from flat_search.residence import ResidentFilter, get_residences
from tests.unit.helper import get_mock_response


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
        156946703,
        87039912,
        156675053,
        156871805,
        154176836,
        147282281,
        156326468,
    ]

    search_filter = ResidentFilter(
        location_identifier="POSTCODE^623999",
        min_bedrooms=2,
        min_price=0,
        max_price=1000000,
        residence_type="flat",
        radius=0.25,
        min_bathrooms=0,
        min_size=0,
        exclusion_list=[],
    )

    with monkeypatch.context() as m:
        m.setattr(requests, "get", get_mock_response(right_move_page))

        expected_result = residences
        actual_result = [
            residence["id"]
            for residence in get_residences(residence_filter=search_filter)
        ]

    assert expected_result == actual_result


def test_duplicates(monkeypatch, right_move_page_duplicates):
    """test duplicate entries determined by their id"""

    residences = [147763901]

    with monkeypatch.context() as m:
        m.setattr(requests, "get", get_mock_response(right_move_page_duplicates))

        expected_result = residences
        actual_result = [residence["id"] for residence in get_residences()]

    assert expected_result == actual_result


def test_exclude_list(monkeypatch, right_move_page):
    """test exluding residence by id"""

    search_filter = ResidentFilter(
        location_identifier="POSTCODE^623999",
        min_bedrooms=2,
        min_price=0,
        max_price=1000000,
        residence_type="flat",
        radius=0.25,
        min_bathrooms=0,
        min_size=0,
        exclusion_list=[147763901],
    )

    residences = [
        # 147763901,
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
        actual_result = [
            residence["id"]
            for residence in get_residences(residence_filter=search_filter)
        ]

    assert expected_result == actual_result
