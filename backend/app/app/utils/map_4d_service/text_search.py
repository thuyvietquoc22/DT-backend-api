import requests
from sqlalchemy.util import raise_

from app.exceptions.param_invalid_exception import ParamInvalidException
from app.utils.map_4d_service import TextSearchResponse
from app.utils.map_4d_service.base_service import BaseMap4DService
from app.utils.map_4d_service.config import Map4DConfig
from app.utils.map_4d_service.response import Map4DServiceResponse


class Map4DTextSearchService(BaseMap4DService):
    @property
    def url(self):
        return "http://api.map4d.vn/sdk/place/text-search"

    def __init__(self, config: Map4DConfig):
        self.config = config

    def fetch(
            self,
            text: str = None,
            types: str = None,
            location: str = None
    ) -> Map4DServiceResponse[TextSearchResponse]:
        if text is None and location is None:
            raise ParamInvalidException("Text or location is required")

        data = {
            "key": self.config.api_key,
            "text": text,
            "types": types,
            "location": location,
        }

        api_url = self.build_url(**{k: v for k, v in data.items() if v is not None})

        response = requests.request("GET", api_url).text

        return Map4DServiceResponse[TextSearchResponse].model_validate_json(response)
