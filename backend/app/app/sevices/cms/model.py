from bson import ObjectId
from click import BadParameter

from app.decorator import signleton
from app.decorator.parser import parse_as
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.cms.assets import AssetsResponse
from app.models.cms.model import ModelCreate, ModelResponse, Location, ModelUpdate, ModelType
from app.models.pagination_model import Pageable
from app.repository.cms.model import ModelRepository
from app.sevices.cms.assets import AssetsService


@signleton.singleton
class ModelService:
    def __init__(self):
        self.repo = ModelRepository()
        self.assets_service = AssetsService()

    @parse_as(ModelResponse)
    def create_model(self, model: ModelCreate):

        assets: list[AssetsResponse] = self.assets_service.find_by_ids([model.asset_id])

        # Find Assets
        if not assets or len(assets) != 1:
            raise ParamInvalidException("Assets not found")

        model.asset_id = ObjectId(model.asset_id)

        return self.repo.create(model)

    @parse_as(list[ModelResponse])
    def get_all(self, pageable: Pageable):
        result = self.repo.get_models(pageable)
        return result

    @parse_as(list[ModelResponse])
    def get_by_id(self, model_id):
        return self.repo.get_by_id(model_id)

    @parse_as(list[ModelResponse])
    def get_by_area(self, start: Location, end: Location, limit):
        if start == end:
            raise BadParameter("Start and End Location must be different")
        return self.repo.get_by_area(start, end, limit)

    def delete_by_id(self, model_id):
        delete_response = self.repo.delete(model_id)
        if delete_response.deleted_count == 0:
            raise Exception("Model not found")

    def update_model(self, model_id: str, model: ModelUpdate):
        return self.repo.update(model_id, model)

    def delete_by_asset_id(self, asset_id: str):
        delete_response = self.repo.delete_by_asset_id(asset_id)
        if delete_response.deleted_count == 0:
            raise Exception("Model not found")
        return delete_response.deleted_count

    def validate_asset(self, model_type: ModelType, asset_ids: list[str]) -> list[AssetsResponse]:
        assets: list[AssetsResponse] = self.assets_service.find_by_ids(asset_ids)

        # Find Assets
        if not assets or len(assets) != len(asset_ids):
            raise ParamInvalidException("Assets not found")

        # Check Assets Type and Quantity
        if model_type == "2D":
            if len(assets) != 1:
                raise ParamInvalidException("2D model must have only 1 asset")
            else:
                if assets[0].type != "image":
                    raise ParamInvalidException("2D model must have 'image' asset")
        elif model_type == "3D":
            if len(assets) != 2:
                raise ParamInvalidException("3D model must have 2 assets")
            else:
                assets_type = [asset.type for asset in assets]
                if "3d_object" not in assets_type:
                    raise ParamInvalidException("3D model must have '3d_object' asset")
                if "texture" not in assets_type:
                    raise ParamInvalidException("3D model must have 'texture' asset")

        return assets

    def get_group_by_model_id(self, model_id):
        return self.repo.get_group_by_model_id(model_id)

    def get_models_by_group(self, group: list[str], pageable: Pageable):
        result = self.repo.get_models_by_group(group, pageable)
        return result