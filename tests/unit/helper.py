"""helper functions testing including mocks"""

from flat_search.residence import ResidentFilter


def get_mock_response(response):
    """callable response for reqequest mocking"""

    def mock_response(*args, **kwargs):  # pylint: disable=unused-argument
        """mock response"""
        return MockResponse(response)

    return mock_response


class MockResponse:  # pylint: disable=too-few-public-methods
    """mock response object"""

    def __init__(self, response=None):
        self.text = response


def build_filter(
    location_identifier=None,
    min_bedrooms=None,
    min_price=None,
    max_price=None,
    residence_type=None,
    radius=None,
    min_bathrooms=None,
    min_size=None,
    exclusion_list=None,
):  # pylint: disable=too-many-arguments,too-many-positional-arguments
    """default filter object for testing support with overrides"""
    return ResidentFilter(
        location_identifier=(
            "POSTCODE^623743" if not location_identifier else location_identifier
        ),
        min_bedrooms=0 if not min_bedrooms else min_bedrooms,
        min_price=0 if not min_price else min_price,
        max_price=9999999 if not max_price else max_price,
        residence_type="flat" if not residence_type else residence_type,
        radius=0 if not radius else radius,
        min_bathrooms=0 if not min_bathrooms else min_bathrooms,
        min_size=0 if not min_size else min_size,
        exclusion_list=[] if not exclusion_list else exclusion_list,
    )
