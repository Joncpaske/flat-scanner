"""happy path integration tests calling rightmove"""

from flat_search.residence import (
    ResidentFilter,
    get_agent,
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
        min_bedrooms=0,
        min_price=0,
        residence_type="flat",
        radius=0,
        min_bathrooms=0,
        min_size=0,
        exclusion_list=[],
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
        exclusion_list=[
            87039912,
            150252452,
            156094826,
            142204871,
            157255367,
            157991846,
        ],
    )

    result = []
    for residence in get_residences(residence_filter=residences_filter):
        result.append(
            f"{get_id(residence)}, {get_size(residence)}, {get_price(residence)}, \
                {get_bathroom_count(residence)}, {get_bedroom_count(residence)}, \
                    https://www.rightmove.co.uk{get_url_path(residence)}, {get_agent(residence)}\n"
        )

    assert True
