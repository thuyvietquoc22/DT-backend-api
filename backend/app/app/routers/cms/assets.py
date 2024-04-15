from typing import Annotated

from fastapi import APIRouter, UploadFile, Form, Body

from app.sevices.cms.assets import AssetsService
from app.models.cms.assets import AssetsResponse, GroupAssets
from app.models.pagination_model import Pageable, PaginationResponse


class AssetsRouter:

    def __init__(self):
        self.asset_service = AssetsService()

    @property
    def router(self):
        router = APIRouter(prefix='/assets', tags=['Assets'])

        @router.get('', response_model=PaginationResponse[AssetsResponse])
        def get_all_assets(page: int = 1, limit: int = 10):
            pageable = Pageable(page=page, limit=limit)
            result = self.asset_service.get_all_assets(pageable=pageable)
            return PaginationResponse.response_pageable(data=result, pageable=pageable)

        @router.get('/group', response_model=list[GroupAssets])
        def get_all_group_asset():
            return self.asset_service.get_group()

        @router.get('/name', response_model=list[dict])
        def get_all_name_asset():
            return self.asset_service.get_names()

        @router.get('/get-id', response_model=dict)
        def find_id_by_public_id(public_id: str):
            result: list[AssetsResponse] = self.asset_service.find_by_public_id(public_id)
            if result and len(result) > 0:
                return {
                    "_id": result[0].id,
                }

        @router.get('/{asset_id}', response_model=AssetsResponse)
        def get_asset_by_id(asset_id: str):
            assets = self.asset_service.find_by_ids([asset_id])
            if not assets:
                raise Exception("Asset not found")

            return assets[0]

        @router.get('/count-usage/{asset_id}')
        def count_usage(asset_id: str):
            return self.asset_service.count_usage(asset_id)

        @router.post('', response_model=AssetsResponse)
        def upload_assets(object_3d: UploadFile, texture: UploadFile, image: UploadFile, name: Annotated[str, Form()],
                          group_id: Annotated[str, Form()]):
            result = self.asset_service.upload_assets(object_3d, texture, image, name, group_id)
            return result[0]

        @router.delete('/{asset_id}')
        def delete_asset_by_id(asset_id: str):
            asset, deleted = self.asset_service.delete_by_id(asset_id)
            return {
                "deleted": deleted,
                "message": f"Đã xoá {deleted} model và asset \"{asset.name}\""
            }

        @router.patch('/rename/{asset_id}', response_model=AssetsResponse)
        def rename_assets_by_id(asset_id: str, name: Annotated[str, Body(...)]):
            return self.asset_service.update_name_by_id(asset_id, name)

        @router.patch('/file/{asset_id}', response_model=AssetsResponse)
        def update_file_by_id(asset_id: str, object_3d: UploadFile = None, texture: UploadFile = None,
                              image: UploadFile = None):
            return self.asset_service.update_content_by_id(asset_id, object_3d, texture, image)

        return router
