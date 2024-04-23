from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.controller import controller_collection
from app.decorator.parser import parse_as
from app.decorator.signleton import singleton
from app.models.desktop.control import ControlType, BaseController
from app.models.desktop.control.camera import CameraControl
from app.models.desktop.control.vms_sign import VMSSignController
from app.models.pagination_model import Pageable
from app.repository.base_repository import BaseRepository


@singleton
class ControlRepository(BaseRepository[BaseController, BaseController, BaseController]):

    @property
    def collection(self) -> Collection:
        return controller_collection

    @property
    def pipeline(self):
        return []

    def get_last_control(self, device_id: str, control_type: ControlType):
        pipeline = self.pipeline + [
            {'$match': {'device_id': ObjectId(device_id), 'control_type': control_type}},
            {'$sort': {'time_control': -1}},
            {'$limit': 1}
        ]
        return self.collection.aggregate(pipeline)

    @parse_as(response_type=CameraControl, get_first=True)
    def get_last_camera_control(self, device_id: str):
        return self.get_last_control(device_id, "CAMERA")

    @parse_as(response_type=VMSSignController, get_first=True)
    def get_last_vms_sign_control(self, vms_sign_id):
        return self.get_last_control(vms_sign_id, "VMS_SIGN")

    def get_history_control(self, device_id, pageable: Pageable):
        query = {
            'device_id': ObjectId(device_id)
        }
        pipeline = self.pipeline + [
            {'$match': query},
            {'$sort': {'time_control': -1}},
            {'$skip': pageable.skip},
            {'$limit': pageable.limit}
        ]
        self.get_pageable(pageable, query)
        return self.collection.aggregate(pipeline)
