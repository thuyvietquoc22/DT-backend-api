from pymongo.collection import Collection

from app.db.mongo.address import address_collection
from app.decorator import signleton
from app.decorator.parser import parse_as
from app.models.desktop.master_data.address import ProvinceResponse, DistrictResponse


@signleton.singleton
class AddressRepository:
    @property
    def address_collection(self) -> Collection:
        return address_collection

    @parse_as(response_type=list[ProvinceResponse])
    def get_all_provinces(self, name):
        query = {}
        if name not in [None, ""]:
            query["name"] = {"$regex": f".*{name}.*", "$options": "i"}

        pipeline = [
            {"$match": query},
            {"$sort": {"name": 1}}
        ]
        result = self.address_collection.aggregate(pipeline=pipeline)
        return result

    @parse_as(response_type=ProvinceResponse)
    def get_province_by_code(self, code):
        return self.address_collection.find_one({"code": code})

    @parse_as(response_type=DistrictResponse, get_first=True)
    def get_district_by_code(self, district_code):
        pipeline = [
            {'$unwind': '$districts'},
            {"$addFields": {'districts.province_code': '$code'}},
            {'$replaceRoot': {'newRoot': '$districts'}},
            {'$match': {'code': district_code}}
        ]

        return self.address_collection.aggregate(pipeline=pipeline)
