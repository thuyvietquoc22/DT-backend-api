from bson import ObjectId

from app.core.password_encoder import hash_password
from app.models.desktop.traffic_light import TrafficLightCreate, TrafficLightUpdate
from app.repository.cms.model import ModelRepository
from app.repository.desktop.traffic_light import TrafficLightRepository, traffic_light_repo


class TrafficLightDomain:

    @property
    def traffic_light_repo(self) -> TrafficLightRepository:
        return traffic_light_repo

    @property
    def model_repo(self) -> ModelRepository:
        return ModelRepository()

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

        traffic_light_create.id_model = ObjectId(model_id)
        traffic_light_create.password = hash_password(traffic_light_create.password)

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
            raise Exception("Đèn tín hiệu này chưa xoá")


traffic_light_domain = TrafficLightDomain()
