from fastapi import APIRouter

from app.routers import BaseRouter, CMSTag
from app.sevices.cms.account import AccountService
from app.models import StringBody
from app.models.auth.admin_auth import AccountRegisterModel
from app.models.cms.account import AccountUpdate, AccountResponse
from app.models.pagination_model import Pageable, PaginationResponse


class AccountRouter(BaseRouter):

    @property
    def account_service(self):
        return AccountService()

    @property
    def router(self):
        router = APIRouter(prefix='/accounts', tags=CMSTag().get("Account"))

        @router.get('/', response_model=PaginationResponse[AccountResponse])
        def get_accounts(limit: int = 10, page: int = 1, fullname: str = None, email: str = None):
            pageable = Pageable.of(limit=limit, page=page)
            response = self.account_service.get_all_accounts(pageable, fullname, email)
            return PaginationResponse.response_pageable(response, pageable)

        @router.get('/{_id}')
        def get_account_by_id(_id: str):
            return self.account_service.get_account_by_id(_id)

        @router.post('/')
        def create_account(account_create: AccountRegisterModel):
            self.account_service.create_account(account_create)
            return {"message": "Create account success"}

        @router.put('/{_id}')
        def update_account(_id: str, account_update: AccountUpdate):
            self.account_service.update_account(_id, account_update)
            return {"message": "Update account success"}

        @router.patch('/password/{_id}')
        def update_password_by_id(_id: str, password: StringBody):
            result = self.account_service.update_password_by_id(_id, password.content)
            return {"message": "Update password success"} if result else {"message": "Update password failed"}

        @router.delete('/{_id}')
        def delete_account(_id: str):
            delete_result = self.account_service.delete_account_by_id(_id)
            if not delete_result or delete_result.deleted_count == 0:
                return {"message": "Account not found"}
            else:
                return {"message": "Delete account success"}

        return router
