from fastapi import APIRouter, Body

from app.domain.admin.account import AccountDomain
from app.models import StringBody
from app.models.admin.account import AccountUpdate
from app.models.auth.admin_auth import AccountRegisterModel
from app.models.pagination_model import Pageable


class AccountRouter:

    @property
    def account_domain(self):
        return AccountDomain()

    @property
    def router(self):
        router = APIRouter(prefix='/accounts', tags=['System Account'])

        @router.get('/')
        def get_accounts(limit: int = 10, page: int = 1, name: str = None, email: str = None):
            pageable = Pageable.of(limit=limit, page=page)
            return self.account_domain.get_all_accounts(pageable, name, email)

        @router.get('/{_id}')
        def get_account_by_id(_id: str):
            return self.account_domain.get_account_by_id(_id)

        @router.post('/')
        def create_account(account_create: AccountRegisterModel):
            self.account_domain.create_account(account_create)
            return {"message": "Create account success"}

        @router.put('/{_id}')
        def update_account(_id: str, account_update: AccountUpdate):
            self.account_domain.update_account(_id, account_update)
            return {"message": "Update account success"}

        @router.patch('/password/{_id}')
        def update_password_by_id(_id: str, password: StringBody):
            result = self.account_domain.update_password_by_id(_id, password.content)
            return {"message": "Update password success"} if result else {"message": "Update password failed"}

        @router.delete('/{_id}')
        def delete_account(_id: str):
            delete_result = self.account_domain.delete_account_by_id(_id)
            if not delete_result or delete_result.deleted_count == 0:
                return {"message": "Account not found"}
            else:
                return {"message": "Delete account success"}

        return router
