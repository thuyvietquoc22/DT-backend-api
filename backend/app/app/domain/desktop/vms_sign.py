from bson import ObjectId

from app.core.password_encoder import hash_password
from app.decorator.parser import parse_as
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.cms.model import ModelResponse
from app.models.desktop.vms_sign import VMSSignCreate
from app.repository.cms.model import ModelRepository
from app.repository.desktop.connect_source import connection_source_repo
from app.repository.desktop.cross_road import CrossRoadRepo, cross_road_repo
from app.repository.desktop.vms_sign import VMSSignRepository, vms_sign_repo
from app.utils.common import calculate_bound


class VMSSignDomain:

    @property
    def vms_sign_repo(self) -> VMSSignRepository:
        return vms_sign_repo

    @property
    def model_repo(self) -> ModelRepository:
        return ModelRepository()

    @property
    def cross_road_repo(self) -> CrossRoadRepo:
        return cross_road_repo

    @property
    def connect_source_repo(self):
        return connection_source_repo

    @parse_as(ModelResponse, True)
    def get_model_by_id(self, model_id: str):
        return self.model_repo.get_by_id(model_id)

    def create_vms_sign(self, vms_sign_create: VMSSignCreate):
        # Check model is existed
        model_id = vms_sign_create.id_model
        model = self.get_model_by_id(model_id)

        if not model:
            raise ParamInvalidException("Không tìm thấy Model")

        # Check model is in vms sign group
        group = self.model_repo.get_group_by_model_id(model_id)
        if not group:
            raise ParamInvalidException("Không xát định được nhóm của model")
        elif group.keyname != "VMS_SIGN":
            raise ParamInvalidException("Model không thuộc nhóm VMS Sign")

        # Check connection source is existed
        connection_source = self.connect_source_repo.find_connection_source_by_keyname(vms_sign_create.resource)
        if not connection_source:
            raise ParamInvalidException("Không tìm thấy Connection Source")

        vms_sign_create.id_model = ObjectId(model_id)
        vms_sign_create.password = hash_password(vms_sign_create.password)

        self.vms_sign_repo.create(vms_sign_create)

    def update_vms_sign(self, vms_sign_id, vms_sign_update):
        self.vms_sign_repo.update(vms_sign_id, vms_sign_update)

    def get_all_vms_sign(self):
        return self.vms_sign_repo.get_all_vms_sign()

    def get_vms_sign_by_id(self, vms_sign_id):
        return self.vms_sign_repo.get_vms_sign_by_id(vms_sign_id)

    def get_vms_sign_nearby(self, cross_road_id, distance=1000):
        cross_road = self.cross_road_repo.get_cross_road_by_id(cross_road_id)

        if not cross_road:
            raise ParamInvalidException(f"Không tìm thấy điểm giao nào với id \"{cross_road_id}\"")

        min_lat, max_lat, min_lng, max_lng = calculate_bound(cross_road.location.lat, cross_road.location.lng, distance)
        return self.vms_sign_repo.get_vms_sign_inside_bound(min_lat, max_lat, min_lng, max_lng)

    def delete_vms_sign(self, vms_sign_id):
        self.vms_sign_repo.delete(vms_sign_id)


vms_sign_domain = VMSSignDomain()
