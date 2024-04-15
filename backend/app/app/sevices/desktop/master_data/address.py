from app.repository.desktop.master_data.address import AddressRepository


class AddressService:

    @property
    def address_repo(self) -> AddressRepository:
        return AddressRepository()

    def get_all_provinces(self, name):
        return self.address_repo.get_all_provinces(name)

    def get_province_by_code(self, code):
        return self.address_repo.get_province_by_code(code)


