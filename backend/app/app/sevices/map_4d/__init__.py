import numpy
from loguru import logger
from scipy.spatial import distance

from app.core.config import settings
from app.decorator.signleton import singleton
from app.models.cms.model import Location
from app.sevices.map_4d.config import Map4DConfig
from app.sevices.map_4d.geo_code import Map4DGeoCodeService
from app.sevices.map_4d.nearby_search import Map4DNearbySearchService
from app.sevices.map_4d.place_detail import Map4DPlaceDetailService
from app.sevices.map_4d.text_search import Map4DTextSearchService


@singleton
class Map4DService:

    def __init__(self):
        self._config = Map4DConfig(api_key=settings.MAP_4D_KEY)
        self.geo_code = Map4DGeoCodeService(self._config)
        self.text_search = Map4DTextSearchService(self._config)
        self.place_detail = Map4DPlaceDetailService(self._config)
        self.nearby_search = Map4DNearbySearchService(self._config)

    def get_crossroad_location(self, first_street: str, second_street: str, district: str):
        """
        Get the location of the crossroad between two streets in the same district
        """
        first_result = self.text_search.fetch(text=f"{first_street} {district}", types="street")
        second_result = self.text_search.fetch(text=f"{second_street} {district}", types="street")

        if not first_result or not first_result.results or len(first_result.results) == 0:
            logger.error(f"Cannot find location for '{first_street} {district}'")
            return None, None
        if not second_result or not second_result.results or len(second_result.results) == 0:
            logger.error(f"Cannot find location for '{second_street} {district}'")
            return None, None

        first_id = first_result.results[0].id
        second_id = second_result.results[0].id

        first_place_detail = self.place_detail.fetch(first_id)
        if not first_place_detail or not first_place_detail.result:
            logger.error(f"Cannot find place detail for '{first_street} {district}'")
            return None, None
        first_coords = first_place_detail.result.flat_coordinates  # List of points

        second_place_detail = self.place_detail.fetch(second_id)
        if not second_place_detail or not second_place_detail.result:
            logger.error(f"Cannot find place detail for '{second_street} {district}'")
            return None, None
        second_coords = second_place_detail.result.flat_coordinates  # List of points

        if not first_coords or len(first_coords) == 0:
            logger.error(f"Cannot find coordinates for '{first_street} {district}'")
            return None, None
        if not second_coords or len(second_coords) == 0:
            logger.error(f"Cannot find coordinates for '{second_street} {district}'")
            return None, None

        # Calculate pairwise distances between points in first_coords and second_coords
        pairwise_distances = distance.cdist(first_coords, second_coords, 'euclidean')

        # Find the indices of the minimum distance
        min_indices = numpy.unravel_index(numpy.argmin(pairwise_distances), pairwise_distances.shape)

        try:
            # Get the coordinates of the points with minimum distance
            point1 = first_coords[min_indices[0]]
            point2 = second_coords[min_indices[1]]
            return point1, point2
        except IndexError:
            logger.error(f"Cannot find location for '{first_street} {district}' and '{second_street} {district}'")
            return None, None


# a = Map4DService().nearby_search.fetch(Location(lat=16.033219, lng=108.217095), radius=100, types="street")
# print(str(a))