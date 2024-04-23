from bson import ObjectId

import app.db.mongo.connection_source
from app.decorator.parser import parse_val_as
from app.decorator.signleton import singleton
from app.exceptions.param_invalid_exception import ParamInvalidException

from app.models.desktop.master_data.bus_connection import BaseBusConnection, BusConnectionCreate, BusConnectionResponse, \
    BusConnectionUpdate
from app.models.desktop.master_data.bus_routes import BusRoutesResponse
from app.models.pagination_model import Pageable
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
        self.check_connection_source(bus_connection)

        # Check bus router id
        bus_router = self.bus_router_repo.get_by_id(bus_connection.bus_router_id)
        bus_router = parse_val_as(bus_router, BusRoutesResponse, True)
        if not bus_router:
            raise ParamInvalidException("Bus router not found")

        # Encoded bus password
        bus_connection.password = RSAHelper.instance().encrypt_message(bus_connection.password)

        self.bus_connection_repo.create_bus_connection([bus_connection])

    def list_bus_connections(self, pageable: Pageable):
        result = self.bus_connection_repo.get_all(pageable)
        return parse_val_as(result, list[BusConnectionResponse])

    def get_bus_connection(self, bus_connection_id: str):
        result = self.bus_connection_repo.get_by_id(bus_connection_id)
        return parse_val_as(result, BusConnectionResponse, True)

    def update_bus_connection(self, bus_connection_id, bus_connection: BusConnectionUpdate):

        if bus_connection.connection_source is not None:
            self.check_connection_source(bus_connection)

        if bus_connection.password:
            bus_connection.password = self.rsa_helper.encrypt_message(bus_connection.password)

        if bus_connection.bus_router_id is not None:
            bus_router = self.bus_router_repo.get_by_id(bus_connection.bus_router_id)
            bus_router = parse_val_as(bus_router, BusRoutesResponse, True)
            if not bus_router:
                raise ParamInvalidException("Bus router not found")

        result = self.bus_connection_repo.update(bus_connection_id, bus_connection)
        return parse_val_as(result, BusConnectionResponse, True)

    def check_connection_source(self, bus_connection):
        connection_source = self.connection_source.find_connection_source_by_keyname(
            app.db.mongo.connection_source.connection_source)
        if not connection_source:
            raise ParamInvalidException("Connection source not found")

    def delete_bus_connection(self, bus_connection_id):
        return self.bus_connection_repo.delete(bus_connection_id)
