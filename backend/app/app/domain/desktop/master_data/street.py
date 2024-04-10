from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.desktop.master_data.street import StreetCreate
from app.repository.desktop.master_data.address import AddressRepository
from app.repository.desktop.master_data.street import StreetRepository


class StreetDomain:
    def __init__(self):
        self.street_repo = StreetRepository()
        self.address_repo = AddressRepository()

    def find_all_by_districts(self, districts_id):
        return self.street_repo.find_all_by_district(districts_id)

    def create_street(self, street_create: StreetCreate):
        # Check district_code is exist
        districts = [self.address_repo.get_district_by_code(i) for i in street_create.district_code]
        for district in districts:
            if district is None:
                raise ParamInvalidException("District code invalid")

        return self.street_repo.create(street_create)

    def update_street(self, street_id, street_create):
        return self.street_repo.update(street_id, street_create)

    def delete_street(self, street_id):
        return self.street_repo.delete(street_id)
