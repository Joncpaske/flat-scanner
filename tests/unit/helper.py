"""helper functions testing including mocks"""


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
