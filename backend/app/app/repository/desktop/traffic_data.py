from datetime import datetime

from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo_db import traffic_data_collection
from app.decorator import signleton
from app.decorator.parser import parse_as
from app.models.desktop.camera import CameraTrafficDataResponse
from app.models.desktop.traffic_data import TrafficDataResponse
from app.repository.base_repository import BaseRepository
from app.repository.desktop.master_data.vehicle import VehicleTypeRepository
from app.utils.timer import TimerHelper


@signleton.singleton
class TrafficDataRepository(BaseRepository):

    def __init__(self):
        self.all_vehicle_type = VehicleTypeRepository().get_all_vehicle_type()

    @property
    def collection(self) -> Collection:
        return traffic_data_collection

    def insert_many_traffic_data(self, data):
        return self.collection.insert_many([i.dict() for i in data])

    @parse_as(response_type=list[TrafficDataResponse])
    def get_traffic_data_by_camera_id(self, camera_id, minute_ago):
        time: datetime = TimerHelper.get_time_ago(minute_ago)
        pipeline = [
            {"$match": {"camera_id": ObjectId(camera_id), "time": {"$gte": time}}},
            {"$sort": {"time": -1}},
            {"$limit": 1}
        ]

        return self.collection.aggregate(pipeline)

    def get_current_capacity(self, camera: CameraTrafficDataResponse):
        # Get current traffic data last 3 minutes
        __current__ = 7 * 24 * 60  # 7 Day

        traffic_data = camera.live_passage_capacity

        # Check if current_traffic_data is empty
        if not traffic_data or len(traffic_data) == 0:
            raise Exception("No traffic data found")

        current_traffic_data = traffic_data[0]

        # Calculate current capacity
        current_capacity = 0
        for data in current_traffic_data.vehicle_count:
            current_capacity += data.count * self.get_size(data.vehicle_type)

        return current_capacity, traffic_data[0].time

    def get_size(self, vehicle_type):
        for item in self.all_vehicle_type:
            if item.type == vehicle_type:
                return item.size
        raise Exception("Vehicle type not found")
