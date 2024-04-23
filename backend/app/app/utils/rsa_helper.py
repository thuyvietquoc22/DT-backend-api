import os

import rsa

from app.core.config import settings


class RSAHelper:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def encrypt_message(self, text: str):
        return text

    def decrypt_message(self, encrypted_message):
        return encrypted_message
