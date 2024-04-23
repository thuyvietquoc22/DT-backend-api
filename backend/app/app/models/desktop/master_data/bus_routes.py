from typing import Optional

from bson import ObjectId
from pydantic import field_serializer

from app.models import BaseMongoModel
from app.models.cms.model import Location
from app.models.desktop.master_data import bus_connection
from app.models.desktop.master_data.bus_connection import BaseBusConnection, BusConnectionCreate


class BaseBusRoutes(BaseMongoModel):
    name: str
    location: Location


class BusStopResponse(BaseMongoModel):
    name: str
    location: Location


class BusRoutesResponse(BaseMongoModel):
    name: str
    bus_stops: list[BusStopResponse]


class BusRoutesCreate(BaseMongoModel):
    name: str
    province_code: int
    start_bus_station_id: str
    end_bus_station_id: str
    bus_stops_id: list[str]
    bus_connections: list[BaseBusConnection] = []

    @field_serializer("bus_stops_id")
    def validate_bus_stops_id(self, value) -> list[ObjectId]:
        return [ObjectId(id_) for id_ in value]

    @field_serializer("end_bus_station_id", "start_bus_station_id")
    def serialize_bus_station_id(self, value) -> ObjectId:
        return ObjectId(value)


class BusRoutesUpdate(BaseMongoModel):
    name: Optional[str] = None
    province_code: Optional[int] = None
    start_bus_station_id: Optional[str] = None
    end_bus_station_id: Optional[str] = None
    bus_stops_id: Optional[list[str]] = None

    @field_serializer("bus_stops_id")
    def validate_bus_stops_id(self, value) -> list[ObjectId]:
        return [ObjectId(id_) for id_ in value]

    @field_serializer("end_bus_station_id", "start_bus_station_id")
    def serialize_bus_station_id(self, value) -> ObjectId:
        return ObjectId(value) if value else None
