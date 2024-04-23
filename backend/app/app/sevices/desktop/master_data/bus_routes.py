from app.decorator import signleton
from app.decorator.parser import parse_val_as
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.desktop.master_data.bus_routes import BusRoutesCreate, BusRoutesResponse, BusRoutesUpdate
from app.repository.cms.model import ModelRepository
from app.repository.desktop.master_data.address import AddressRepository
from app.repository.desktop.master_data.bus_routes import BusRoutesRepository
from app.repository.desktop.master_data.connect_source import ConnectSourceRepository
from app.sevices.desktop.master_data.bus_connection import BusConnectionService


@signleton.singleton
class BusRouteService:

    def __init__(self):
        # SERVICE
        self.bus_connection = BusConnectionService()

        #  REPOSITORY
        self.model_repo = ModelRepository()
        self.bus_routes_repo = BusRoutesRepository()
        self.connect_repo = ConnectSourceRepository()
        self.address_repo = AddressRepository()

    def validate_bus_station(self, bus_router):
        start_bus_station_id = bus_router.start_bus_station_id
        end_bus_station_id = bus_router.end_bus_station_id
        station_ids = []
        if start_bus_station_id is not None:
            station_ids.append(start_bus_station_id)

        if end_bus_station_id is not None:
            station_ids.append(end_bus_station_id)

        model_ids = station_ids + (bus_router.bus_stops_id or [])
        model_ids = set(model_ids)

        if model_ids is None or len(model_ids) == 0:
            return None

        models = self.model_repo.get_list_models_by_ids(model_ids)
        if len(models) != len(model_ids):
            raise ParamInvalidException("Model not found")
        for model in models:
            model_keyname = model.asset.group.keyname
            if model.id in station_ids and model_keyname != "BUS_STATION":
                raise ParamInvalidException(f"Model <{model.name} ({model.id})> is not bus station")

            if model_keyname not in ["BUS_STATION", "BUS_STOP"]:
                raise ParamInvalidException(f"Model <{model.name}> ({model.id}) is not bus station or bus stop")

    def create_bus_router(self, bus_router: BusRoutesCreate):
        self.validate_bus_station(bus_router)
        self.validate_province_code(bus_router.province_code)

        result = self.bus_routes_repo.create_bus_router(bus_router)

        # TODO Create bus connections
        if bus_router.bus_connections and len(bus_router.bus_connections) > 0:
            self.bus_connection.create_bus_connections(bus_router.bus_connections, result.id)
            # self.create_bus_connection(bus_router)

        return result

    def list_bus_stop(self):
        return self.model_repo.get_bus_stop()

    def validate_province_code(self, province_code: int):
        if not self.address_repo.get_province_by_code(province_code):
            raise ParamInvalidException(f"Not found province with code {province_code}")

    def list_bus_routes(self, pageable):
        result = self.bus_routes_repo.get_all(pageable)
        return parse_val_as(result, list[BusRoutesResponse])

    def update_bus_router(self, bus_routes_id, bus_router: BusRoutesUpdate):

        self.validate_bus_station(bus_router)

        if bus_router.province_code is not None:
            self.validate_province_code(bus_router.province_code)

        result = self.bus_routes_repo.update(bus_routes_id, bus_router)

    def delete_bus_router(self, bus_routes_id):
        return self.bus_routes_repo.delete(bus_routes_id)

    def get_bus_router(self, bus_routes_id):
        result = self.bus_routes_repo.get_by_id(bus_routes_id)
        return parse_val_as(result, BusRoutesResponse, True)
