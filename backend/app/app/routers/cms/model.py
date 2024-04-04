from fastapi import APIRouter

from app.domain.cms.model import ModelDomain
from app.models.cms.model import ModelCreate, ModelResponse, Location, ModelUpdate
from app.models.pagination_model import Pageable


class ModelRouter:

    def __init__(self, model_domain: ModelDomain):
        self.model_domain = model_domain

    @property
    def router(self):
        router = APIRouter(prefix="/models", tags=["Model 2D, 3D"])

        @router.get("", response_model=list[ModelResponse])
        async def get_models(page: int = 1, limit: int = 999):
            pageable = Pageable.of(page=page, limit=limit)
            result = self.model_domain.get_all(pageable=pageable)
            return result
            # return PaginationResponse.response_pageable(data=result, pageable=pageable)

        @router.post("/area", response_model=list[ModelResponse])
        async def get_models_by_area(start: Location, end: Location, limit: int = 20):
            result = self.model_domain.get_by_area(start, end, limit)
            return result

        @router.get("/{model_id}", response_model=ModelResponse)
        async def get_model_by_id(model_id: str):
            try:
                result = self.model_domain.get_by_id(model_id)
                return result[0]
            except IndexError:
                raise Exception("Model not found")

        @router.post("", response_model=ModelResponse)
        async def create_model(model: ModelCreate):
            result = self.model_domain.create_model(model)
            return result

        @router.post("/create-models", response_model=list[ModelResponse])
        async def create_model(model: list[ModelCreate]):
            return [self.model_domain.create_model(m) for m in model]

        @router.delete("/{model_id}")
        async def delete_model_by_id(model_id: str):
            self.model_domain.delete_by_id(model_id)
            return {"message": "Delete success"}

        @router.patch("/{model_id}")
        async def update_model_by_id(model_id: str, model: ModelUpdate):
            self.model_domain.update_model(model_id, model)
            return {"message": "Update success"}

        return router
