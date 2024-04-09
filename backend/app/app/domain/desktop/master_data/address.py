from app.repository.desktop.master_data.address import address_repo, AddressRepo


class AddressDomain:

    @property
    def address_repo(self) -> AddressRepo:
        return address_repo

    def get_all_provinces(self, name):
        return self.address_repo.get_all_provinces(name)

    def get_province_by_code(self, code):
        return self.address_repo.get_province_by_code(code)


address_domain = AddressDomain()
