from app.repository.desktop.master_data.vehicle import VehicleTypeRepository


class VehicleTypeService:

    def __init__(self):
        self.vehicle_type_repo = VehicleTypeRepository()

    def get_all_vehicle_type(self):
        return self.vehicle_type_repo.get_all_vehicle_type()

    def update_size_vehicle_type(self, value: int, vehicle_type_id: str):
        return self.vehicle_type_repo.update_vehicle_type(value, vehicle_type_id)

    def update_vehicle_type(self, vehicle_type, vehicle_type_id):
        return self.vehicle_type_repo.update(vehicle_type_id, vehicle_type)
