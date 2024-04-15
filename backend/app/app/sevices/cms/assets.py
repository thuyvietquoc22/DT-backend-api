from bson import ObjectId
from cloudinary import uploader
from fastapi import UploadFile

from app.decorator.parser import parse_as
from app.models.cms.assets import AssetsCreate, AssetsResponse
from app.models.pagination_model import Pageable
from app.repository.cms.assets import AssetsModelRepository
from app.repository.cms.model import ModelRepository
from app.sevices import BaseService
from app.utils.random_helper import random_str


class AssetsService(BaseService):
    def __init__(self):
        self.assets_repo = AssetsModelRepository()

    @parse_as(list[AssetsResponse])
    def get_all_assets(self, pageable: Pageable):
        return self.assets_repo.get_all_assets(pageable)

    # @staticmethod
    # def check_existed(name: str, assets_type: AssetsType):
    #     try:
    #         response = resource(f"/{assets_type}/{name}")
    #         return response is not None
    #     except NotFound as e:
    #         return False

    @parse_as(list[AssetsResponse])
    def upload_assets(self, object_3d: UploadFile, texture: UploadFile, image: UploadFile, name: str, group_id: str):

        # Check if group_id exists
        group = self.assets_repo.get_group_by_id(group_id)
        if not group:
            raise Exception("Group not found. Check your group_id")

        public_id = random_str(10)

        # Upload 3d object
        obj_3d_url = self.upload_file(object_3d, f"{public_id}.obj", "3d_object")

        # Upload texture
        texture_url = self.upload_file(texture, public_id, "texture")

        # Upload image
        image_url = self.upload_file(image, public_id, "image")

        # Save to Database
        assets = AssetsCreate(name=name, object_3d=obj_3d_url, texture=texture_url, image=image_url,
                              public_id=public_id, group_id=ObjectId(group_id))

        result = self.assets_repo.create_asset(assets)

        return result

    @staticmethod
    def upload_file(file, public_id, assets_type):
        # Handle file type and name
        param = {"folder": assets_type, 'unique_filename': True, 'overwrite': False, }
        if assets_type == "3d_object":
            param['resource_type'] = "raw"
        # Upload to Cloudinary
        upload_info = uploader.upload_resource(file.file, public_id=public_id, **param)
        url = upload_info.url
        return url

    @parse_as(list[AssetsResponse])
    def find_by_ids(self, ids: list[str]):
        result = self.assets_repo.get_assets_by_ids(ids)
        return result

    def delete_by_id(self, asset_id):

        asset: AssetsResponse = self.find_by_ids([asset_id])[0]

        if not asset:
            raise Exception("Asset not found")

        # # Delete from Cloudinary
        # cloud_deleted = uploader.destroy(asset.public_id, resource_type=asset.resource_type)
        #
        # if not cloud_deleted or cloud_deleted.get("result") != "ok":
        #     raise Exception("Cloudinary delete failed")

        # Delete object_file from Cloudinary
        obj_deleted = uploader.destroy(f"object_3d/{asset.public_id}.obj", resource_type="raw")
        texture_deleted = uploader.destroy(f"texture/{asset.public_id}", resource_type="image")
        image_deleted = uploader.destroy(f"image/{asset.public_id}", resource_type="image")

        # Todo: Check if delete failed

        # Delete from Database
        result = self.assets_repo.delete(asset_id)

        model_deleted = ModelRepository().delete_by_asset_id(asset_id)

        if not result or result.deleted_count != 1:
            raise Exception("Database delete failed")

        return asset, model_deleted.deleted_count

    def update_name_by_id(self, asset_id, name):
        asset: AssetsResponse = self.find_by_ids(asset_id)[0]

        if not asset:
            raise Exception("Asset not found")

        # Update to Database
        result = self.assets_repo.update_name(asset_id, name)

        if not result or result.modified_count != 1:
            raise Exception("Not update to Database")

        asset.name = name
        return asset

    @parse_as(list[dict])
    def get_names(self):
        return self.assets_repo.get_all_name()

    def update_content_by_id(self, asset_id, object_3d: UploadFile = None, texture: UploadFile = None,
                             image: UploadFile = None):
        asset: AssetsResponse = self.get_by_id(asset_id)

        if not asset:
            raise Exception("Asset not found")

        # Update 3d object
        if object_3d:
            obj_3d_url = self.upload_file(object_3d, f"{asset.public_id}.obj", "3d_object")
            if not obj_3d_url:
                raise Exception("3d object upload failed")
            asset.object_3d = obj_3d_url

        if texture:
            texture_url = self.upload_file(texture, asset.public_id, "texture")
            if not texture_url:
                raise Exception("Texture upload failed")
            asset.texture = texture_url

        if image:
            image_url = self.upload_file(image, asset.public_id, "image")
            if not image_url:
                raise Exception("Image upload failed")
            asset.image = image_url

        # Update to Database
        result = self.assets_repo.update_url(asset_id, asset.object_3d, asset.texture, asset.image)

        if not result or result.modified_count != 1:
            raise Exception("Database update failed")

        return asset

    def get_group(self):
        return self.assets_repo.get_all_group()

    @parse_as(list[AssetsResponse])
    def find_by_public_id(self, public_id: str):
        if not public_id.startswith("__"):
            public_id = f"__{public_id}"

        return self.assets_repo.find_by_public_id(public_id)

    def count_usage(self, asset_id):
        return self.assets_repo.count_usage(asset_id)

