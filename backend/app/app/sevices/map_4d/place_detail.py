import requests

from app.sevices import BaseService
from app.sevices.map_4d import Map4DConfig
from app.sevices.map_4d.base_map_service import BaseMap4DService
from app.sevices.map_4d.response.place_detail import PlaceDetailResponse


class Map4DPlaceDetailService(BaseMap4DService):

    def __init__(self, config: Map4DConfig):
        self.config = config

    @property
    def url(self):
        return "https://api-app.map4d.vn/map/place/detail"

    def fetch(self, id_: str):
        api_url = f"{self.url}/{id_}"
        response = requests.request("GET", api_url).text

        return PlaceDetailResponse.model_validate_json(response)
