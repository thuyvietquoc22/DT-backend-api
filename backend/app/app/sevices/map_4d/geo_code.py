import requests

from app.models.cms.model import Location
from app.models.desktop.passage_capacity import Bounce
from app.sevices.map_4d.base_map_service import BaseMap4DService
from app.sevices.map_4d.config import Map4DConfig
from app.sevices.map_4d.response.geo_code import GeoCodeResponse


class Map4DGeoCodeService(BaseMap4DService):
    def __init__(self, config: Map4DConfig):
        self.config = config

    @property
    def url(self):
        return "https://api.map4d.vn/sdk/v2/geocode"

    def fetch(self, location: Location = None, address: str = None, bounce: Bounce = None):
        query = {
            "key": self.config.api_key,
        }

        if location is not None:
            query['location'] = str(location)

        if address is not None:
            query['address'] = address

        if bounce is not None:
            query['bounce'] = str(bounce)

        response = requests.request("GET", self.url, params=query)

        return GeoCodeResponse.model_validate_json(response.text)
