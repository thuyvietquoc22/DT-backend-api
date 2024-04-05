import rsa


class RSAHelper:
    _instance = None
    _private_key = ""
    _public_key = ""

    def __init__(self):
        raise Exception("Use instance() method")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def generate_key(self, saved_key=True):
        public_key, private_key = rsa.newkeys(1024)

        self._public_key = public_key
        self._private_key = private_key

        if saved_key:
            with open("public.pem", "wb") as f:
                f.write(public_key.save_pkcs1("PEM"))
            with open("private.pem", "wb") as f:
                f.write(private_key.save_pkcs1("PEM"))

        return public_key, private_key

    def encrypt_message(self, text: str):
        rsa.encrypt(text.encode(), self._public_key)

    def decrypt_message(self, encrypted_message):
        return rsa.decrypt(encrypted_message, self._private_key).decode()

    def set_private_key(self, key):
        self._private_key = rsa.PrivateKey.load_pkcs1(key)

    def set_public_key(self, key):
        self._public_key = rsa.PublicKey.load_pkcs1(key)


a = RSAHelper.instance()
a.generate_key()
encrypted = a.encrypt_message("Hello")
print(a.decrypt_message(encrypted))
