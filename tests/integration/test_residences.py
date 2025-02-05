"""happy path integration tests calling rightmove"""

from flat_search.residence import (
    ResidentFilter,
    get_bathroom_count,
    get_bedroom_count,
    get_id,
    get_price,
    get_residences,
    get_size,
    get_url_path,
)


def test_get_residences():
    """test with minimal level filters"""

    residences_filter = ResidentFilter(
        locationIdentifier="POSTCODE^623743",
        min_bedrooms=2,
        min_price=400000,
        residence_type="flat",
        radius=0.25,
        min_bathrooms=0,
        min_size=0,
    )

    for _ in get_residences(residence_filter=residences_filter):
        pass


def test_get_residences_filter():
    """test with stricter filters"""

    residences_filter = ResidentFilter(
        locationIdentifier="POSTCODE^623743",
        min_bedrooms=2,
        min_price=400000,
        residence_type="flat",
        radius=0.25,
        min_bathrooms=2,
        min_size=800,
    )

    result = []
    for residence in get_residences(residence_filter=residences_filter):
        result.append(
            f"{get_id(residence)}, {get_size(residence)}, {get_price(residence)}, \
                {get_bathroom_count(residence)}, {get_bedroom_count(residence)}, \
                    https://www.rightmove.co.uk{get_url_path(residence)}\n"
        )
