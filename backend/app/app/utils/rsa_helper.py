import os

import rsa

from app.core.config import settings


class RSAHelper:
    _instance = None
    _private_key = None
    _public_key = None

    def __init__(self):
        raise Exception("Use instance() method")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

            key_path: str = settings.RSA_KEY_PATH or "rsa_key/"

            if not os.path.exists(key_path):
                os.makedirs(key_path)

            try:
                with open(key_path + "public.pem", "rb") as f:
                    cls._public_key = rsa.PublicKey.load_pkcs1(f.read())
            except FileNotFoundError as e:
                raise Exception(f"RSA key not found at: {key_path}")

        return cls._instance

    def _load_private_key(self):
        key_path: str = settings.RSA_KEY_PATH or "rsa_key/"

        try:
            with open(key_path + "private.pem", "rb") as f:
                self._private_key = rsa.PrivateKey.load_pkcs1(f.read())
        except FileNotFoundError as e:
            raise Exception(f"RSA key not found at: {key_path}")

    def generate_key(self, saved_key=True):
        public_key, private_key = rsa.newkeys(1024)

        self._public_key = public_key
        self._private_key = private_key

        if True:
            with open("public.pem", "wb") as f:
                f.write(public_key.save_pkcs1("PEM"))
            with open("private.pem", "wb") as f:
                f.write(private_key.save_pkcs1("PEM"))

        return public_key, private_key

    def encrypt_message(self, text: str):
        return rsa.encrypt(text.encode("utf-8"), self._public_key)

    def decrypt_message(self, encrypted_message):
        if not self._private_key:
            self._load_private_key()

        return rsa.decrypt(encrypted_message, self._private_key).decode()

    def set_private_key(self, key):
        self._private_key = rsa.PrivateKey.load_pkcs1(key)

    def set_public_key(self, key):
        self._public_key = rsa.PublicKey.load_pkcs1(key)
