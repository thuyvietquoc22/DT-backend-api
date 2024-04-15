from pymongo.cursor import Cursor

from app.decorator.parser import parse_as
from app.models.cms.permission import PermissionResponse
from app.repository.cms.permission import PermissionRepository
from app.sevices import BaseService


class PermissionService(BaseService):

    def __init__(self, repo: PermissionRepository):
        self.repo = repo

    @parse_as(response_type=list[PermissionResponse])
    def get_all(self):
        result = self.repo.get_all()
        return result

    # Lấy tất cả các permission có phân cấp cha con
    @parse_as(response_type=list[PermissionResponse])
    def get_all_by_id(self, ids: list[str] = None, group: bool = True):
        if group or ids is None:
            return self.__get_all_by_id(ids)
        else:
            return self.__get_all_by_id_not_group(ids)

    def __get_all_by_id(self, ids: list[str]):
        result: Cursor = self.repo.get_all()
        return result

    # Lấy danh sách permission theo id truyền vào không phân cấp cha con
    def __get_all_by_id_not_group(self, permission_ids: list[str]):
        return self.repo.get_permission_by_id(permission_ids)
