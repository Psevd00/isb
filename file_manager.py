import json
import os
from cryptography.hazmat.primitives import serialization

class FileManager:
    def __init__(self, settings_file='settings.json'):
        self.settings_file = settings_file
        self.settings = self._load_default_settings()

    def _load_default_settings(self):
        return {
            'initial_file': 'input.txt',
            'encrypted_file': 'encrypted.txt',
            'decrypted_file': 'decrypted.txt',
            'symmetric_key': 'symmetric_key.txt',
            'public_key': 'public_key.txt',
            'secret_key': 'secret_key.txt',
            'encrypted_symmetric_key': 'enc_symmetric_key.txt'
        }

    def load_settings(self):
        try:
            with open(self.settings_file) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_settings()
            return self.settings

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def save_key(self, path, key, is_binary=False):
        mode = 'wb' if is_binary else 'w'
        with open(path, mode) as f:
            if is_binary and isinstance(key, bytes):
                f.write(key)
            else:
                f.write(key)

    def load_key(self, path, is_binary=False):
        mode = 'rb' if is_binary else 'r'
        with open(path, mode) as f:
            return f.read()

    def save_rsa_key(self, path, key, is_public=True):
        if is_public:
            key_data = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
        else:
            key_data = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
        self.save_key(path, key_data)