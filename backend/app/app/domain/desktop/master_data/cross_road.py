from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.desktop.master_data.cross_road import CrossRoadCreate
from app.repository.desktop.master_data.address import address_repo, AddressRepository
from app.repository.desktop.master_data.cross_road import cross_road_repo, CrossRoadRepo


class CrossRoadDomain:

    @property
    def cross_road_repo(self) -> CrossRoadRepo:
        return cross_road_repo

    @property
    def address_repo(self) -> AddressRepository:
        return address_repo

    def get_district_code(self, district_code: int):
        return self.address_repo.get_district_by_code(district_code)

    def create_cross_road(self, creator_cross_road: CrossRoadCreate):

        district = self.get_district_code(creator_cross_road.district_code)

        if district is None:
            raise ParamInvalidException(f"Mã quận/huyện \"{creator_cross_road.district_code}\" không tồn tại")

        creator_cross_road.province_code = district.province_code

        return self.cross_road_repo.create(creator_cross_road)

    def get_all_cross_road(self):
        return self.cross_road_repo.find_all_cross_road()

    def get_cross_road_by_district_id(self, district_id):
        return self.cross_road_repo.find_cross_road_by_district_id(district_id)

    def get_cross_road_by_id(self, cross_road_id: str):
        return self.cross_road_repo.get_cross_road_by_id(cross_road_id)


cross_road_domain = CrossRoadDomain()
