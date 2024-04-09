from datetime import datetime

from bson import ObjectId

from app.decorator.parser import parse_as
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.cms.model import ModelResponse
from app.models.desktop.control.vms_sign import VMSSignController, VMSSignRequest
from app.models.desktop.vms_sign import VMSSignCreate
from app.models.pagination_model import Pageable
from app.repository.cms.model import ModelRepository
from app.repository.desktop.controller import ControlRepository
from app.repository.desktop.master_data.connect_source import connection_source_repo
from app.repository.desktop.master_data.cross_road import cross_road_repo
from app.repository.desktop.master_data.vms_component import VMSComponentRepository
from app.repository.desktop.vms_sign import vms_sign_repo
from app.utils.common import calculate_bound
from app.utils.rsa_helper import RSAHelper


class VMSSignDomain:

    def __init__(self):
        self.vms_sign_repo = vms_sign_repo
        self.cross_road_repo = cross_road_repo
        self.connect_source_repo = connection_source_repo
        self.model_repo = ModelRepository()
        self.control_repo = ControlRepository()
        self.vms_comp = VMSComponentRepository()

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
        vms_sign_create.password = RSAHelper.instance().encrypt_message(vms_sign_create.password).hex()

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

    def control_vms_sign(self, vms_sign_id: str, controller: VMSSignRequest):
        vms_sign = self.vms_sign_repo.get_vms_sign_by_id(vms_sign_id)

        # Check device is existed
        if not vms_sign:
            raise ParamInvalidException("Không tìm thấy VMS Sign")

        # Check component is existed
        component_ids = [component.vms_component_id for component in controller.images]
        components = self.vms_comp.get_by_ids(component_ids)
        if len(components) != len(controller.images):
            missing_ids = set(component_ids) - {component.id for component in components}
            raise ParamInvalidException(f"Không tìm thấy các component với id {missing_ids}")

        # Set previous state
        last_control = self.control_repo.get_last_vms_sign_control(vms_sign_id)

        control = VMSSignController(
            texts=controller.texts,
            images=controller.images,
            prev_control="",
            time_control=datetime.now(),
            device_id="",
        )
        control.device_id = ObjectId(vms_sign_id)
        control.prev_control = None if last_control is None else ObjectId(last_control.id)

        # Convert id in images to ObjectId
        for image in control.images:
            image.vms_component_id = ObjectId(image.vms_component_id)

        # Todo send control to device

        self.control_repo.create(control)

    @parse_as(response_type=list[VMSSignController])
    def get_history_vms_sign_control(self, vms_sign_id, pageable: Pageable):
        result = self.control_repo.get_history_control(vms_sign_id, pageable)
        return [control for control in result if control.get("control_type") == "VMS_SIGN"]

    @parse_as(response_type=list[VMSSignController])
    def get_vms_sign_by_model_id(self, model_id):
        return self.vms_sign_repo.get_vms_sign_by_model_id(model_id)


vms_sign_domain = VMSSignDomain()
