from bson import ObjectId

from app.core.password_encoder import hash_password
from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models.auth.admin_auth import AccountRegisterModel
from app.models.cms.account import AccountCreate, AccountUpdate
from app.models.pagination_model import Pageable
from app.repository.cms.account import AccountRepository


class AccountService:

    @property
    def account_repository(self):
        return AccountRepository()

    def get_all_accounts(self, pageable: Pageable, name: str, email: str):
        return self.account_repository.find_all(pageable, name, email)

    def get_account_by_id(self, _id: str):
        result = self.account_repository.get_account_by_id(_id)
        return result[0] if result and len(result) > 0 else None

    def delete_account_by_id(self, _id):
        return self.account_repository.delete(_id)

    def check_exist_email(self, email):
        return self.account_repository.find_by_email(email)

    def create_account(self, account_creator: AccountRegisterModel):
        exist_account = self.check_exist_email(account_creator.email)

        if exist_account:
            raise ParamInvalidException("Email này đã được sử dụng")

        account_creator.password = hash_password(account_creator.password)

        account = AccountCreate(
            username=account_creator.username,
            fullname=account_creator.fullname,
            email=account_creator.email,
            password=account_creator.password,
            role_id=ObjectId(account_creator.role_id),
            is_active=True,
            first_login=True
        )

        return self.account_repository.create(account)

    def update_password_by_id(self, _id, password):
        hashed = hash_password(password)
        return self.account_repository.update_password_by_id(_id, hashed)

    def update_account(self, _id, account_update: AccountUpdate):
        if account_update.role_id not in [None, ""]:
            account_update.role_id = ObjectId(account_update.role_id)
        return self.account_repository.update(_id, account_update)
