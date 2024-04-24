from typing import Literal

from fastapi import UploadFile

from app.decorator import signleton
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.desktop.master_data.vms_component import VMSComponentCreate, VMSComponentUpdate
from app.repository.desktop.master_data.vms_component import VMSComponentRepository
from app.repository.desktop.master_data.vms_component_category import VMSComponentCategoryRepository
from app.utils.cloudinary import CloudinaryHelper


@signleton.singleton
class VMSComponentService:

    def __init__(self):
        self.vms_component_repo = VMSComponentRepository()
        self.vms_category_repo = VMSComponentCategoryRepository()

    def create_vms_component(self, image: UploadFile, name: str, type_component: Literal["IMAGE", "ARROW"], code: int,
                             meaning: str, category_key: str):

        # Check category exist
        category = self.vms_category_repo.check_keyname_exist(category_key)
        if not category:
            raise ParamInvalidException(f"Category not found with keyname: {category_key}")

        # Check code exist
        exist_vms_comp = self.vms_component_repo.get_vms_component_by_code_type(code, type_component)
        if exist_vms_comp:
            raise ParamInvalidException(f"Đã ồn tại code: {code}")

        # Handle save to database
        creator = VMSComponentCreate(
            name=name,
            category_key=category_key,
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
        if update_data.category_key is not None:
            # Check category exist
            category = self.vms_category_repo.check_keyname_exist(update_data.category_key)
            if not category:
                raise ParamInvalidException(f"Category not found with keyname: {update_data.category_key}")

        # Check code exist
        comp_type = update_data.type
        if update_data.code is not None and comp_type is not None:
            exist_vms_comp = self.vms_component_repo.get_vms_component_by_code_type(update_data.code, comp_type)
            if exist_vms_comp:
                raise ParamInvalidException(
                    f"Đã ồn tại {'mũi tên' if comp_type == 'ARROW' else 'ảnh'} có  code: {update_data.code}")
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
        url = CloudinaryHelper().upload_file(file=image, folder=vms_comp.folder)

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

    def get_vms_component_by_type(self, tag_name):
        return self.vms_component_repo.get_vms_component_by_type(tag_name)
