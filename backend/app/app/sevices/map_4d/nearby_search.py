import requests

from app.models.cms.model import Location
from app.sevices.map_4d.base_map_service import BaseMap4DService
from app.sevices.map_4d.config import Map4DConfig
from app.sevices.map_4d.response.geo_code import GeoCodeResponse


class Map4DNearbySearchService(BaseMap4DService):
    def __init__(self, config: Map4DConfig):
        self.config = config

    @property
    def url(self):
        return "http://api.map4d.vn/sdk/place/nearby-search"

    def fetch(self, location: Location, radius: int = 1000, types: str = None, text: str = None, tags: str = None):
        # Tags, text, types need exist at once of them
        if not types and not text and not tags:
            raise ValueError("At least one of types, text, tags must be provided")

        query = {
            "key": self.config.api_key,
            "location": str(location),
            "radius": radius,
        }

        if types:
            query['types'] = types

        if text:
            query['text'] = text

        if tags:
            query['tags'] = tags

        response = requests.request("GET", self.url, params=query)

        return GeoCodeResponse.model_validate_json(response.text)
