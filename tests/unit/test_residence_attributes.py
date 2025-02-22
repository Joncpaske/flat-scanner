"""unit tests for residnce module covering residence attributes"""

from flat_search.residence import (
    get_agent,
    get_bathroom_count,
    get_bedroom_count,
    get_id,
    get_price,
    get_published_date,
    get_size,
    get_url_path,
)


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


def test_get_agent():
    """happy path test - retreive agent from the resident object"""

    residence = {"formattedBranchName": "by Foxtons, Temple Fortune"}

    expected_result = "by Foxtons, Temple Fortune"
    actual_result = get_agent(residence)

    assert expected_result == actual_result
