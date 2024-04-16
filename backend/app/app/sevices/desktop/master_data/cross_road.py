from bson import ObjectId

from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.desktop.master_data.cross_road import CrossRoadCreate, CrossRoadUpdate
from app.models.pagination_model import Pageable
from app.repository.desktop.master_data.address import AddressRepository
from app.repository.desktop.master_data.cross_road import CrossRoadRepository
from app.repository.desktop.master_data.street import StreetRepository
from app.sevices.map_4d import Map4DService


class CrossRoadService:

    def __init__(self):
        self.cross_road_repo = CrossRoadRepository()
        self.address_repo = AddressRepository()
        self.street_repo = StreetRepository()
        self.map4d_service = Map4DService()

    def get_district_code(self, district_code: int):
        return self.address_repo.get_district_by_code(district_code)

    def create_cross_road(self, creator_cross_road: CrossRoadCreate):
        # Check district_code is exist
        district = self.get_district_code(creator_cross_road.district_code)

        if district is None:
            raise ParamInvalidException(f"Mã quận/huyện \"{creator_cross_road.district_code}\" không tồn tại")

        # Check street_ids is exist
        for street_id in creator_cross_road.street_ids:
            street = self.street_repo.find_by_id(street_id)
            if street is None:
                raise ParamInvalidException(f"Không tồn tại đường có id \"{street_id}\"")

        creator_cross_road.street_ids = [ObjectId(street_id) for street_id in creator_cross_road.street_ids]

        creator_cross_road.province_code = district.province_code

        return self.cross_road_repo.create(creator_cross_road)

    def get_all_cross_road(self, pageable: Pageable):
        return self.cross_road_repo.find_all_cross_road(pageable)

    def get_cross_road_by_district_id(self, district_id, pageable: Pageable):
        return self.cross_road_repo.find_cross_road_by_district_id(district_id, pageable)

    def get_cross_road_by_id(self, cross_road_id: str):
        return self.cross_road_repo.get_cross_road_by_id(cross_road_id)

    def validate_street_ids(self, street_ids):
        for street_id in street_ids:
            street = self.street_repo.find_by_id(street_id)
            if street is None:
                raise ParamInvalidException(f"Không tồn tại đường có id \"{street_id}\"")

    def validate_district_code(self, district_code):
        district = self.get_district_code(district_code)
        if district is None:
            raise ParamInvalidException(f"Mã quận/huyện \"{district_code}\" không tồn tại")
        return district.province_code

    def update_cross_road(self, district_id, cross_road_update: CrossRoadUpdate):
        cross_road_update.province_code = None

        if cross_road_update.street_ids:
            self.validate_street_ids(cross_road_update.street_ids)

        if cross_road_update.district_code:
            cross_road_update.province_code = self.validate_district_code(cross_road_update.district_code)

        return self.cross_road_repo.update(district_id, cross_road_update)

    def get_cross_road_location(self, first_street, second_street, district):
        return self.map4d_service.get_crossroad_location(first_street, second_street, district)

    def delete_cross_road(self, cross_road_id):
        return self.cross_road_repo.delete(cross_road_id)
