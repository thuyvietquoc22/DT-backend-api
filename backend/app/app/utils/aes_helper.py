from base64 import b64encode, b64decode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import modes, algorithms, Cipher

from app.core.config import settings


class AESHelper:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    @property
    def key(self):
        return bytes.fromhex(settings.AES_KEY)

    @property
    def iv(self):
        return bytes.fromhex(settings.AES_IV)

    def encrypt_message(self, text: str) -> str:
        # return self.encrypt(text, self.key, self.iv)
        return text

    def decrypt_message(self, encrypted_message) -> str:
        # return self.decrypt(encrypted_message, self.key, self.iv)
        return encrypted_message
    def encrypt(self, plaintext, key, iv):
        if plaintext:
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
            return b64encode(ciphertext).decode()
        return None

    def decrypt(self, ciphertext, key, iv):
        ciphertext = b64decode(ciphertext)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_text.decode()


