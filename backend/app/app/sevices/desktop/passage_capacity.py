from app.models.cms.model import Location
from app.models.desktop.camera import CameraTrafficDataResponse
from app.models.desktop.passage_capacity import Bounce, PassageCapacityValue
from app.repository.desktop.camera import CameraRepository
from app.repository.desktop.master_data.passage_capacity import PassageCapacityRepository
from app.repository.desktop.master_data.street import StreetRepository
from app.repository.desktop.traffic_data import TrafficDataRepository
from app.sevices import BaseService
from app.utils.common import calculate_bound
from app.sevices.map_4d import Map4DService


class PassageCapacityService(BaseService):

    def __init__(self):
        self.camera_repo = CameraRepository()
        self.street_repo = StreetRepository()
        self.traffic_data = TrafficDataRepository()
        self.init_passage_capacity_status()
        self.capacity_status = []

    def init_passage_capacity_status(self):
        capacity_status = PassageCapacityRepository().get_all_passage_capacity_status()
        capacity_status.sort(reverse=True)
        self.capacity_status = capacity_status

    def get_all_passage_capacity(self, bounce: Bounce):
        cameras = self.camera_repo.get_last_data_camera_inside_bound(
            min_lat=bounce.min_lat,
            max_lat=bounce.max_lat,
            min_lng=bounce.min_lng,
            max_lng=bounce.max_lng,
            minute_ago=7749 * 24 * 60  # 7749 Day
        )

        if cameras is None or len(cameras) == 0:
            raise Exception("No camera found in this bounce")

        # Get current passage capacity per camera
        passage_capacities = [self.get_passage_capacity(camera) for camera in cameras]

        return passage_capacities, bounce

    def get_passage_capacity(self, camera: CameraTrafficDataResponse) -> PassageCapacityValue:
        # Get street by camera id
        street = camera.street
        max_passage_capacity = street.passage_capacity

        try:
            # Get Current Capacity in camera
            current_passage_capacity, time = self.traffic_data.get_current_capacity(camera)

            passage_capacity_ratio = round(current_passage_capacity / max_passage_capacity, 2)

            return PassageCapacityValue(
                camera_id=camera.id,
                location=camera.location,
                passage_capacity_current=current_passage_capacity,
                passage_capacity_ratio=passage_capacity_ratio,
                passage_capacity_status=self.get_passage_capacity_status(passage_capacity_ratio),
                street=street,
                at=time
            )
        except Exception as e:
            return PassageCapacityValue(
                camera_id=camera.id,
                location=camera.location,
                passage_capacity_current=0,
                passage_capacity_ratio=0,
                passage_capacity_status=None,
                street=street,
                at=None
            )

    def get_passage_capacity_status(self, passage_capacity_ratio: float):
        for status in self.capacity_status:
            if passage_capacity_ratio >= status.value:
                return status
        raise Exception("Không xát định được trạng thái")

    def get_passage_capacity_by_keyword(self, keyword: str, lat, lng):

        location = []
        if lat is not None and lng is not None:
            location.append(Location(lat=lat, lng=lng))
        else:
            response = Map4DService().text_search.fetch(text=keyword)
            if response is None or response.results is None or len(response.results) == 0:
                raise Exception("Không tìm thấy địa điểm: " + keyword)

            location = [result.location for result in response.results]

        min_lat, max_lat, min_lng, max_lng = calculate_bound(location[0].lat, location[0].lng, 750)
        bounce = Bounce(min_lat=min_lat, max_lat=max_lat, min_lng=min_lng, max_lng=max_lng)

        return self.get_all_passage_capacity(bounce)
