"""residence module - retrieves residence objects from a rightmove search"""

import json
from dataclasses import asdict, dataclass
from typing import Iterable, Literal

import requests
from bs4 import BeautifulSoup

Html = str
PropertyType = Literal["flat"]
Residence = dict[any, any]
Unit = str

RIGHT_MOVE_URL = "https://www.rightmove.co.uk/property-for-sale/find.html"


@dataclass
class ResidentFilter:  # pylint: disable=too-many-instance-attributes
    """Rightmove filter options including client side filters"""

    locationIdentifier: str  # pylint: disable=invalid-name
    min_bedrooms: int
    min_price: int
    residence_type: PropertyType
    radius: float
    min_bathrooms: int
    min_size: int
    exclusion_list: set[int]


def get_residences(
    url=RIGHT_MOVE_URL, residence_filter: ResidentFilter = None
) -> Iterable[Residence]:
    """query Rightmove for properties

    Keyword arguments:
    url - Rightmove address - defaulted to live site
    residence_filter - filter applied to search results server and client side
    """

    params = _get_server_params(residence_filter)
    params["index"] = 0

    ids = set()
    while True:
        r = requests.get(url=url, params=params, timeout=2)
        max_count, residences = _get_residence_objects(r.text)

        for residence in residences:
            if not residence_filter or _valid_residence(residence, residence_filter):

                residence_id = get_id(residence)

                if residence_id not in ids:
                    yield residence
                    ids.add(get_id(residence))

            params["index"] += 1

        if params["index"] >= max_count:
            break


def _get_residence_objects(page: Html) -> tuple[int, list[dict[any, any]]]:
    parser = BeautifulSoup(page, "html.parser")

    script = parser.find("script")
    while "window.jsonModel" not in script.text:
        script = script.find_next("script")

    resp = json.loads(script.text.split("window.jsonModel = ")[1])
    return int(resp["resultCount"]), resp["properties"]


def _valid_residence(residence: dict[any, any], residence_filter: ResidentFilter):
    return (
        (
            not get_bathroom_count(residence)
            or get_bathroom_count(residence) >= residence_filter.min_bathrooms
        )
        and (
            not get_size(residence)[1]
            or get_size(residence)[1] >= residence_filter.min_size
        )
        and (get_id(residence) not in residence_filter.exclusion_list)
    )


def _get_server_params(residence_filter: ResidentFilter = None) -> dict[str, str]:
    server_filters = [
        "locationIdentifier",
        "min_bedrooms",
        "min_price",
        "residence_type",
        "radius",
    ]

    return {
        key: val
        for key, val in (asdict(residence_filter).items() if residence_filter else [])
        if key in server_filters
    }


def get_bathroom_count(residence: dict[any, any]) -> int:
    """
    extract residence bathroom count

    Keyword arguments:
    residence - Rightmove residence object
    """
    return residence.get("bathrooms")


def get_bedroom_count(residence: dict[any, any]) -> int:
    """
    extract residence bedroom count

    Keyword arguments:
    residence - Rightmove residence object
    """
    return residence.get("bedrooms")


def get_price(residence: dict[any, any]):
    """
    extract residence price

    Keyword arguments:
    residence - Rightmove residence object
    """
    price = residence.get("price")
    return (price.get("currencyCode"), price.get("amount"))


def get_published_date(residence: dict[any, any]):
    """
    extract date residence was published on rightmove

    Keyword arguments:
    residence - Rightmove residence object
    """
    return residence.get("firstVisibleDate")


def get_size(residence: dict[any, any]):
    """
    extract residence size (metric, value)

    Keyword arguments:
    residence - Rightmove residence object
    """
    size = residence.get("displaySize").split()

    if not size:
        return (None, None)

    val = int(size[0].replace(",", ""))
    unit = " ".join(size[1:])
    return (unit, val)


def get_id(residence: dict[any, any]):
    """
    extract residence id

    Keyword arguments:
    residence - Rightmove residence object
    """
    return residence.get("id")


def get_url_path(residence: dict[any, any]):
    """
    extract residence url

    Keyword arguments:
    residence - Rightmove residence object
    """
    return residence.get("propertyUrl")


def get_agent(residence: Residence):
    """
    extract residence agent publisher

    Keyword arguments:
    residence - Rightmove residence object
    """
    return residence.get("formattedBranchName")
