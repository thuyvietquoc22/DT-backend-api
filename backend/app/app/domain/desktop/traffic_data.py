from datetime import datetime

from app.decorator import signleton
from app.models.desktop.traffic_data import TrafficDataCreate
from app.repository.desktop.traffic_data import TrafficDataRepository


@signleton.singleton
class TrafficDataDomain:
    def __init__(self):
        self.traffic_data_repo = TrafficDataRepository()

    def insert_traffic_data(self, data: list[TrafficDataCreate]):
        for item in data:
            item.time = datetime.now()
        return self.traffic_data_repo.insert_many_traffic_data(data)

    def get_traffic_data_by_camera_id(self, camera_id: str, minute_ago: int):
        return self.traffic_data_repo.get_traffic_data_by_camera_id(camera_id, minute_ago)
