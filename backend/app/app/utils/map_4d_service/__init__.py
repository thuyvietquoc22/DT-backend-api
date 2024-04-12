from abc import abstractmethod

from pydantic import BaseModel

from app.core.config import settings
from app.decorator.signleton import singleton
from app.utils.map_4d_service.config import Map4DConfig
from app.utils.map_4d_service.geo_code import Map4DGeoCodeService
from app.utils.map_4d_service.response.text_search import TextSearchResponse
from app.utils.map_4d_service.text_search import Map4DTextSearchService


@singleton
class Map4DService:
    __api_key__: str = ""
    geo_code: Map4DGeoCodeService = None
    text_search: Map4DTextSearchService = None

    def __init__(self):
        self._config = Map4DConfig(api_key=settings.MAP_4D_KEY)

        self.geo_code = Map4DGeoCodeService(self._config)
        self.text_search = Map4DTextSearchService(self._config)
