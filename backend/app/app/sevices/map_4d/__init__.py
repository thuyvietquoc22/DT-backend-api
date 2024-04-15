from app.core.config import settings
from app.decorator.signleton import singleton
from app.sevices.map_4d.config import Map4DConfig
from app.sevices.map_4d.geo_code import Map4DGeoCodeService
from app.sevices.map_4d.text_search import Map4DTextSearchService


@singleton
class Map4DService:
    __api_key__: str = ""
    geo_code: Map4DGeoCodeService = None
    text_search: Map4DTextSearchService = None

    def __init__(self):
        self._config = Map4DConfig(api_key=settings.MAP_4D_KEY)

        self.geo_code = Map4DGeoCodeService(self._config)
        self.text_search = Map4DTextSearchService(self._config)
