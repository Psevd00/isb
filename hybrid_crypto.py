import os
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from asymmetric import AsymmetricCipher
from symmetric import SymmetricCipher
from file_manager import FileManager
from crypto_utils import CryptoUtils


class HybridCryptoSystem:
    def __init__(self):
        self.file_manager = FileManager()
        self.settings = self.file_manager.load_settings()

    def generate_keys(self, key_size=192):
        sym_key = CryptoUtils.generate_symmetric_key(key_size)
        private_key, public_key = AsymmetricCipher.generate_keys()
        encrypted_sym_key = AsymmetricCipher.encrypt(public_key, sym_key)

        self.file_manager.save_key(
            self.settings['symmetric_key'],
            b64encode(sym_key).decode('utf-8')
        )
        self.file_manager.save_rsa_key(
            self.settings['public_key'],
            public_key
        )
        self.file_manager.save_rsa_key(
            self.settings['secret_key'],
            private_key,
            is_public=False
        )
        self.file_manager.save_key(
            self.settings['encrypted_symmetric_key'],
            b64encode(encrypted_sym_key).decode('utf-8')
        )

    def encrypt_file(self):
        private_key_pem = self.file_manager.load_key(self.settings['secret_key'])
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None,
            backend=default_backend()
        )

        encrypted_sym_key = b64decode(
            self.file_manager.load_key(self.settings['encrypted_symmetric_key'])
        )
        sym_key = AsymmetricCipher.decrypt(private_key, encrypted_sym_key)

        cipher = SymmetricCipher(sym_key)
        plaintext = self.file_manager.load_key(
            self.settings['initial_file'],
            is_binary=True
        )
        iv, ciphertext = cipher.encrypt(plaintext)

        self.file_manager.save_key(
            self.settings['encrypted_file'],
            b64encode(iv + ciphertext).decode('utf-8')
        )

    def decrypt_file(self):
        private_key_pem = self.file_manager.load_key(self.settings['secret_key'])
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None,
            backend=default_backend()
        )

        encrypted_sym_key = b64decode(
            self.file_manager.load_key(self.settings['encrypted_symmetric_key'])
        )
        sym_key = AsymmetricCipher.decrypt(private_key, encrypted_sym_key)

        cipher = SymmetricCipher(sym_key)
        encrypted_data = b64decode(
            self.file_manager.load_key(self.settings['encrypted_file'])
        )
        iv, ciphertext = encrypted_data[:8], encrypted_data[8:]
        plaintext = cipher.decrypt(iv, ciphertext)

        self.file_manager.save_key(
            self.settings['decrypted_file'],
            plaintext,
            is_binary=True
        )