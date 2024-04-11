from fastapi import APIRouter

from app.domain.desktop.passage_capacity import PassageCapacityDomain
from app.models.desktop.passage_capacity import Bounce
from app.routers import BaseRouter


class PassageCapacityRouter(BaseRouter):

    def __init__(self):
        self.passage_capacity_domain = PassageCapacityDomain()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/passage-capacity", tags=["Desktop > Passage Capacity"])

        @router.post("/current")
        def get_all_passage_capacity(bounce: Bounce):
            return self.passage_capacity_domain.get_all_passage_capacity(bounce)

        return router
