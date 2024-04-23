from datetime import datetime

from bson import ObjectId

from app.db.mongo.mongo_db import start_session
from app.decorator import signleton
from app.decorator.parser import parse_as, parse_val_as
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.cms.model import ModelResponse
from app.models.desktop.camera import CameraCreate, CameraResponse
from app.models.desktop.control.camera import CameraControl, CameraControlRequest
from app.repository.cms.model import ModelRepository
from app.repository.desktop.camera import CameraRepository
from app.repository.desktop.controller import ControlRepository
from app.repository.desktop.master_data.connect_source import ConnectSourceRepository
from app.repository.desktop.master_data.cross_road import CrossRoadRepository
from app.repository.desktop.master_data.street import StreetRepository
from app.sevices.desktop.traffic_data import TrafficDataService
from app.utils.common import calculate_bound, is_in_range, copy_attr
from app.utils.rsa_helper import RSAHelper


@signleton.singleton
class CameraService:

    def __init__(self):
        self.camera_repo = CameraRepository()
        self.cross_road_repo = CrossRoadRepository()
        self.connect_source_repo = ConnectSourceRepository()
        self.model_repo = ModelRepository()
        self.control_repo = ControlRepository()
        self.street_repo = StreetRepository()

    def create_camera(self, camera: CameraCreate):

        session = start_session()

        self.check_model(camera)

        self.check_connection_source(camera)

        self.check_street_existed(camera)

        camera.password = RSAHelper.instance().encrypt_message(camera.password).hex()
        # camera.id_model = ObjectId(camera.id_model)
        # camera.street_id = ObjectId(camera.street_id)

        value = self.camera_repo.create(camera)
        value = parse_val_as(value, response_type=CameraResponse, get_first=True)

        # Todo mock data to camera
        TrafficDataService().mock_camera_data(value.id)
        return value

    def check_model(self, camera):
        # Check model
        model = self.get_model_by_id(camera.id_model)
        if not model:
            raise ParamInvalidException(f"Không tìm thấy model với id \"{camera.id_model}\"")
        group = self.model_repo.get_group_by_model_id(camera.id_model)
        if not group:
            raise ParamInvalidException(f"Không xát định được model đang thuộc về nhóm nào")
        elif group.keyname != "CAMERA":
            raise ParamInvalidException(f"Model không thuộc nhóm CAMERA")

    def check_connection_source(self, camera):
        # Check connection source is existed
        connection_source = self.connect_source_repo.find_connection_source_by_keyname(camera.resource)
        if not connection_source:
            raise ParamInvalidException("Không tìm thấy Connection Source")

    def check_street_existed(self, camera):
        # Check street is existed
        street = self.street_repo.find_by_id(camera.street_id)
        if not street:
            raise ParamInvalidException(f"Không tìm thấy đường đường có id \"{camera.street_id}\"")

    @parse_as(ModelResponse, True)
    def get_model_by_id(self, model_id):
        return self.model_repo.get_by_id(model_id)

    def get_all_camera(self):
        return self.camera_repo.get_all_camera()

    def get_camera_by_id(self, camera_id: str):
        return self.camera_repo.get_camera_by_id(camera_id)

    def get_camera_nearby(self, cross_road_id):

        cross = self.cross_road_repo.get_cross_road_by_id(cross_road_id)

        if not cross:
            raise ParamInvalidException(f"Không tìm thấy điểm giao nào với id \"{cross_road_id}\"")

        min_lat, max_lat, min_lng, max_lng = calculate_bound(cross.location.lat, cross.location.lng)

        return self.camera_repo.get_camera_inside_bound(min_lat, max_lat, min_lng, max_lng)

    def update_camera(self, camera_id, camera):
        self.camera_repo.update(camera_id, camera)

    def delete_camera(self, camera_id):
        deleted = self.camera_repo.delete(camera_id)
        if deleted.deleted_count == 0:
            raise ParamInvalidException(f"Không tìm thấy camera với id \"{camera_id}\"")

    def control_camera(self, camera_control: CameraControlRequest):
        # Validate camera control here
        #     validate in range
        # Todo get min max value from database
        is_in_range(camera_control.angle_x, -180, 180)
        is_in_range(camera_control.angle_y, -180, 180)
        is_in_range(camera_control.iris, 0, 100)
        is_in_range(camera_control.zoom, 0, 100)
        is_in_range(camera_control.focus, 0, 100)

        camera = self.camera_repo.get_camera_by_id(camera_control.camera_id)
        if camera is None:
            raise ParamInvalidException(f"Không tìm thấy camera với id \"{camera_control.camera_id}\"")

        # Set prev state
        prev_control = self.control_repo.get_last_camera_control(device_id=camera_control.camera_id)

        if prev_control is None:
            prev_control = CameraControl(
                prev_control=None,
                time_control=datetime.now(),
                device_id=ObjectId(camera_control.camera_id),
                control_type="CAMERA",
                angle_x=0,
                angle_y=0,
                zoom=0,
                focus=0,
                iris=0
            )

        # Set data prev state if field in camera_control is not exist
        new_control = copy_attr(camera_control, prev_control)
        new_control.prev_control = ObjectId(prev_control.id) if prev_control.id else None
        new_control.time_control = datetime.now()

        # Save control to database
        new_control.id = self.control_repo.create(new_control)

        # Todo Send control to camera

        return new_control

    @parse_as(response_type=list[CameraControl])
    def get_history_control(self, device_id, pageable):
        result = self.control_repo.get_history_control(device_id, pageable)
        return [control for control in result if control.get("control_type") == "CAMERA"]

    def get_camera_by_model_id(self, model_id):
        return self.camera_repo.get_camera_by_model_id(model_id)
