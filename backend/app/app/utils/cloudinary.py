from abc import ABC, abstractmethod

from cloudinary import uploader
from fastapi import UploadFile

from app.decorator import signleton


class CloudinaryEnabler(ABC):

    @property
    @abstractmethod
    def folder(self):
        pass

    @property
    @abstractmethod
    def public_id(self):
        pass


@signleton.singleton
class CloudinaryHelper:
    @staticmethod
    def upload_file(file: UploadFile, public_id=None, folder: str = None, upload_info: CloudinaryEnabler = None) -> str:

        """
        Param public_id, folder will be replaced by upload_info if upload_info is not None
        """
        if upload_info is not None:
            folder = upload_info.folder
            public_id = upload_info.public_id
        # Handle file type and name
        param = {"folder": folder, 'unique_filename': True, 'overwrite': False, }
        if public_id not in [None, '']:
            param['public_id'] = public_id
        # Upload to Cloudinary
        upload_info = uploader.upload_resource(file.file, **param)
        url = upload_info.url
        return url

    @staticmethod
    def delete_file(public_id: str):
        return uploader.destroy(public_id)
