from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.exceptions.param_invalid_exception import ParamInvalidException
from app.models import BaseMongoModel


class AddressLevel(Enum):
    LV_1 = 'province'
    LV_2 = 'district'
    LV_3 = 'ward'
    LV_4 = 'street'


class DivisionType(Enum):
    # Khai báo các giá trị Enum ở đây

    TP_TRUNG_UONG = ('Thành phố trung ương', AddressLevel.LV_1)
    TINH = ('Tỉnh', AddressLevel.LV_1)

    QUAN = ('Quận', AddressLevel.LV_2)
    THANH_PHO = ('Thành phố', AddressLevel.LV_2)
    THI_XA = ('Thị xã', AddressLevel.LV_2)
    HUYEN = ('Huyện', AddressLevel.LV_2)

    PHUONG = ('Phường', AddressLevel.LV_3)
    XA = ('Xã', AddressLevel.LV_3)
    THI_TRAN = ('Thị trấn', AddressLevel.LV_3)


class SimpleAddress(BaseModel):
    name: str
    code: int
    codename: str
    division_type: str

    @property
    def division(self):
        for division_type in DivisionType:
            if division_type.value[0].lower() == self.division_type.lower():
                return division_type
        raise ParamInvalidException(f"Division type {self.division_type} is invalid")


class District(SimpleAddress):
    short_codename: str


class DistrictResponse(District):
    province_code: Optional[int] = None
    pass


class Province(BaseMongoModel, SimpleAddress):
    districts: list[District] = []


class ProvinceResponse(Province):
    """
    Response đầy đủ thông tin của các huyện
    """
    pass


class ProvinceListResponse(BaseMongoModel, SimpleAddress):
    """
    Response chỉ chứa thông tin cơ bản của tỉnh
    """
    pass
