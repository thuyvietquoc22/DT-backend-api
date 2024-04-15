from app.decorator import signleton


@signleton.singleton
class BaseService:
    pass
