from abc import ABC, abstractmethod

from fastapi import APIRouter


class BaseRouter(ABC):

    @property
    @abstractmethod
    def router(self) -> APIRouter:
        pass
