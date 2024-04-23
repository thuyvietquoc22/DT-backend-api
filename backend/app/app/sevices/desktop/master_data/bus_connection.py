from bson import ObjectId

from app.decorator.parser import parse_val_as
from app.decorator.signleton import singleton
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.desktop.master_data.bus_connection import BaseBusConnection, BusConnectionCreate
from app.models.desktop.master_data.bus_routes import BusRoutesResponse
from app.repository.desktop.master_data.bus_connection import BusConnectionRepository
from app.repository.desktop.master_data.bus_routes import BusRoutesRepository
from app.repository.desktop.master_data.connect_source import ConnectSourceRepository
from app.utils.rsa_helper import RSAHelper


@singleton
class BusConnectionService:

    def __init__(self):
        self.connection_source = ConnectSourceRepository()
        self.rsa_helper = RSAHelper.instance()
        self.bus_connection_repo = BusConnectionRepository()
        self.bus_router_repo = BusRoutesRepository()

    def create_bus_connections(self, bus_connections: list[BaseBusConnection], bus_route_id: str):
        # Check connection source
        connections_source_key = set([i.connection_source for i in bus_connections])
        connections_sources = self.connection_source.find_connection_sources_by_keynames(connections_source_key)
        if len(connections_sources) != len(connections_source_key):
            raise Exception("Connection source not found")

        # Encoded bus password
        bus_connections = [
            BusConnectionCreate(
                code=bs.code,
                provider=bs.provider,
                connection_source=bs.connection_source,
                ip_address=bs.ip_address,
                username=bs.username,
                password=RSAHelper.instance().encrypt(bs.password),
                bus_router_id=ObjectId(bus_route_id),
            )
            for bs in bus_connections
        ]

        self.bus_connection_repo.create_bus_connection(bus_connections)

    def create_bus_connection(self, bus_connection: BusConnectionCreate):
        # Check connection source
        connection_source = self.connection_source.find_connection_source_by_keyname(bus_connection.connection_source)
        if not connection_source:
            raise ParamInvalidException("Connection source not found")

        # Check bus router id
        bus_router = self.bus_router_repo.get_by_id(bus_connection.bus_router_id)
        bus_router = parse_val_as(bus_router, BusRoutesResponse, True)
        if not bus_router:
            raise ParamInvalidException("Bus router not found")

        # Encoded bus password
        bus_connection.password = RSAHelper.instance().encrypt(bus_connection.password)

        self.bus_connection_repo.create_bus_connection([bus_connection])
