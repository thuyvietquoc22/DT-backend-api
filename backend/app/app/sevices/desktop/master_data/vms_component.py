from typing import Literal

from fastapi import UploadFile

from app.decorator import signleton
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.desktop.master_data.vms_component import VMSComponentCreate, VMSComponentUpdate
from app.repository.desktop.master_data.vms_component import VMSComponentRepository
from app.utils.cloudinary import CloudinaryHelper


@signleton.singleton
class VMSComponentService:

    def __init__(self):
        self.vms_component_repo = VMSComponentRepository()

    def create_vms_component(self,
                             image: UploadFile,
                             name: str,
                             type_component: Literal["IMAGE", "ARROW"],
                             code: int,
                             meaning: str):
        # Check code exist
        exist_vms_comp = self.vms_component_repo.get_vms_component_by_code(code)

        if exist_vms_comp:
            raise ParamInvalidException(f"Existed VMS Component with code: {code}")

        # Handle save to database
        creator = VMSComponentCreate(
            name=name,
            type=type_component,
            code=code,
            meaning=meaning,
            url=""
        )

        # Handle upload image
        url = CloudinaryHelper().upload_file(file=image, upload_info=creator)

        creator.url = url

        self.vms_component_repo.create(creator)

    def get_all_vms_component(self):
        return self.vms_component_repo.get_all_vms_component()

    def update_vms_component(self, vms_component_id: str, update_data: VMSComponentUpdate):
        self.vms_component_repo.update(vms_component_id, update_data)

    def get_vms_component_by_id(self, vms_component_id):
        return self.vms_component_repo.get_vms_component_by_id(vms_component_id)

    def get_vms_component_by_code(self, code):
        return self.vms_component_repo.get_vms_component_by_code(code)

    def update_vms_component_image(self, vms_component_id: str, image: UploadFile):
        vms_comp = self.vms_component_repo.get_vms_component_by_id(vms_component_id)
        if not vms_comp:
            raise ParamInvalidException(f"VMS Component not found with id: {vms_component_id}")
        # Handle upload image
        url = CloudinaryHelper().upload_file(file=image, upload_info=vms_comp)

        try:
            # Delete old image
            CloudinaryHelper().delete_file(vms_comp.public_id)
        except Exception as e:
            pass

        # Handle save to database
        self.vms_component_repo.update_url_vms_component_by_id(vms_component_id, url)

    def delete_vms_component(self, vms_component_id):
        vms_comp = self.get_vms_component_by_id(vms_component_id)

        if not vms_comp:
            raise ParamInvalidException(f"VMS Component not found with id: {vms_component_id}")

        CloudinaryHelper().delete_file(vms_comp.public_id)

        self.vms_component_repo.delete(vms_component_id)
