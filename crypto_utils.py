import os
from base64 import b64encode, b64decode

class CryptoUtils:
    @staticmethod
    def generate_symmetric_key(key_size=192):
        return os.urandom(key_size // 8)

    @staticmethod
    def b64_encode(data):
        return b64encode(data).decode('utf-8')

    @staticmethod
    def b64_decode(data):
        return b64decode(data)

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')