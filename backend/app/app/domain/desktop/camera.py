from bson import ObjectId

from app.core.password_encoder import hash_password
from app.decorator.parser import parse_as
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.cms.model import ModelResponse
from app.models.desktop.camera import CameraCreate
from app.repository.cms.model import ModelRepository
from app.repository.desktop.camera import CameraRepository, camera_repo
from app.repository.desktop.cross_road import CrossRoadRepo, cross_road_repo


class CameraDomain:

    @property
    def camera_repo(self) -> CameraRepository:
        return camera_repo

    @property
    def model_repo(self) -> ModelRepository:
        return ModelRepository()

    @property
    def cross_road_repo(self) -> CrossRoadRepo:
        return cross_road_repo

    def create_camera(self, camera: CameraCreate):
        # Check model
        model = self.get_model_by_id(camera.model_id)

        if not model:
            raise ParamInvalidException(f"Không tìm thấy model với id \"{camera.model_id}\"")

        camera.password = hash_password(camera.password)
        camera.model_id = ObjectId(camera.model_id)

        self.camera_repo.create(camera)

    @parse_as(ModelResponse, True)
    def get_model_by_id(self, model_id):
        return self.model_repo.get_by_id(model_id)

    def get_all_camera(self):
        return self.camera_repo.get_all_camera()

    def get_camera_by_id(self, camera_id: str):
        return self.camera_repo.get_camera_by_id(camera_id)

    def get_camera_nearby(self, cross_road_id):
        DISTANCE = 1000  # Unit: meters

        cross = self.cross_road_repo.get_cross_road_by_id(cross_road_id)

        if not cross:
            raise ParamInvalidException(f"Không tìm thấy điểm giao nào với id \"{cross_road_id}\"")

        min_lat, max_lat, min_lng, max_lng = self.calculate_bound(cross.location.lat, cross.location.lng, DISTANCE)

        return self.camera_repo.get_camera_inside_bound(min_lat, max_lat, min_lng, max_lng)

    def calculate_bound(self, lat: float, lng: float, distance: int):
        return (
            lat - distance * 0.00001,
            lat + distance * 0.00001,
            lng - distance * 0.00001,
            lng + distance * 0.00001
        )

    def update_camera(self, camera_id, camera):
        self.camera_repo.update(camera_id, camera)


camera_domain = CameraDomain()
