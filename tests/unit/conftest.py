"""pylint conftest storing shared fixtures"""

import importlib

import pytest

from tests import resources


@pytest.fixture(scope="session")
def resource_dir():
    """resource directory located in tests/resources"""

    with importlib.resources.path(resources) as r:
        yield r


@pytest.fixture(scope="session")
def right_move_page(resource_dir):  # pylint: disable=redefined-outer-name
    """default page copied from right move search result"""

    with open(resource_dir / "testpage.html", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="session")
def right_move_page_duplicates(resource_dir):  # pylint: disable=redefined-outer-name
    """default page copied from right move search result"""

    with open(resource_dir / "testpagewithduplicates.html", encoding="utf-8") as f:
        return f.read()
