from bson import ObjectId

from app.decorator import signleton
from app.decorator.parser import parse_as
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.cms.model import ModelResponse
from app.models.desktop.traffic_light import TrafficLightCreate, TrafficLightUpdate
from app.repository.cms.model import ModelRepository
from app.repository.desktop.master_data.connect_source import ConnectSourceRepository
from app.repository.desktop.master_data.cross_road import CrossRoadRepository
from app.repository.desktop.traffic_light import TrafficLightRepository
from app.utils.common import calculate_bound
from app.utils.aes_helper import AESHelper


@signleton.singleton
class TrafficLightService:

    def __init__(self):
        self.traffic_light_repo = TrafficLightRepository()
        self.model_repo = ModelRepository()
        self.cross_road_repo = CrossRoadRepository()
        self.connect_source_repo = ConnectSourceRepository()

    @parse_as(ModelResponse, True)
    def get_model_by_id(self, model_id: str):
        return self.model_repo.get_by_id(model_id)

    def create_traffic_light(self, traffic_light_create: TrafficLightCreate):
        # Check model is existed
        model_id = traffic_light_create.id_model
        model = self.get_model_by_id(model_id)

        if not model:
            raise Exception("Không tìm thấy Model")

        # Check model is in traffic group
        group = self.model_repo.get_group_by_model_id(model_id)
        if not group:
            raise Exception("Không xát định được nhóm của model")
        elif group.keyname != "TRAFFIC_LIGHT":
            raise Exception("Model không thuộc nhóm traffic")

        # Check connection source is existed
        connection_source = self.connect_source_repo.find_connection_source_by_keyname(traffic_light_create.resource)
        if not connection_source:
            raise ParamInvalidException("Không tìm thấy Connection Source")

        traffic_light_create.id_model = ObjectId(model_id)
        traffic_light_create.password = AESHelper.instance().encrypt_message(traffic_light_create.password).hex()

        self.traffic_light_repo.create(traffic_light_create)

    def update_traffic_light(self, _id: str, traffic_light: TrafficLightUpdate):

        self.traffic_light_repo.update(_id, traffic_light)

    def get_all_traffic_light(self):
        return self.traffic_light_repo.get_all_traffic_light()

    def get_traffic_light_by_id(self, traffic_light_id):
        return self.traffic_light_repo.get_traffic_light_by_id(traffic_light_id)

    def delete_traffic_light(self, traffic_light_id):
        deleted = self.traffic_light_repo.delete(traffic_light_id)
        if not deleted or deleted.deleted_count == 0:
            raise Exception("Đèn tín hiệu này chưa được xoá")

    def get_traffic_light_nearby(self, cross_road_id, distance=1000):
        cross_road = self.cross_road_repo.get_cross_road_by_id(cross_road_id)

        if not cross_road:
            raise ParamInvalidException(f"Không tìm thấy điểm giao nào với id \"{cross_road_id}\"")

        min_lat, max_lat, min_lng, max_lng = calculate_bound(cross_road.location.lat, cross_road.location.lng, distance)

        return self.traffic_light_repo.get_traffic_light_inside_bound(min_lat, max_lat, min_lng, max_lng)

    def get_traffic_light_by_model_id(self, model_id):
        return self.traffic_light_repo.get_traffic_light_by_model_id(model_id)

    def get_traffic_light_by_cross_road_id(self, cross_road_id):
        return self.traffic_light_repo.get_traffic_light_by_cross_road_id(cross_road_id)
