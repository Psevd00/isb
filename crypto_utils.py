import os

class CryptoUtils:
    @staticmethod
    def generate_symmetric_key(key_size=192):
        return os.urandom(key_size // 8)

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
