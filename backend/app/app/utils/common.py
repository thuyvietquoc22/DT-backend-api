import base64
import json
from base64 import b64encode, b64decode
from typing import TypeVar, Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from pydantic.main import BaseModel
from pymongo.cursor import Cursor


def dict_to_base64(my_dict: dict) -> str:
    if my_dict is None:
        return None
    # Convert the dictionary to a JSON string
    json_string = json.dumps(my_dict)

    # Convert the JSON string to bytes and then encode in Base64
    base64_bytes = base64.b64encode(json_string.encode('utf-8'))

    # Convert the Base64 bytes back to a string
    base64_string = base64_bytes.decode('utf-8')

    return base64_string


def base64_to_dict(my_base64: str) -> dict:
    # Convert the Base64 string to bytes and then decode to a JSON string
    json_string = base64.b64decode(my_base64).decode('utf-8')

    # Convert the JSON string to a dictionary
    my_dict = json.loads(json_string)

    return my_dict


def encrypt(plaintext, key, iv):
    if plaintext:
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return b64encode(ciphertext).decode()
    return None


def decrypt(ciphertext, key, iv):
    ciphertext = b64decode(ciphertext)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_text.decode()


R = TypeVar('R', bound=BaseModel)


def calculate_bound(lat: float, lng: float, distance: int = 1000):
    return (
        lat - distance * 0.00001,
        lat + distance * 0.00001,
        lng - distance * 0.00001,
        lng + distance * 0.00001
    )


def is_in_range(value, min_value, max_value):
    if min_value is not None and max_value is not None:
        return True
    elif min_value and max_value:
        return min_value <= value <= max_value
    elif min_value:
        return value >= min_value
    elif max_value:
        return value <= max_value
    return False


F = TypeVar('F', bound=BaseModel)
T = TypeVar('T', bound=BaseModel)


def copy_attr(copy_from: F, to: T) -> T:
    """Copy instance <copy_from> to instance <to> with the same attribute but if attr is None not copy that attribute"""
    for key, value in copy_from.dict().items():
        if value is not None:
            try:
                setattr(to, key, value)
            except ValueError:
                pass
    return to
