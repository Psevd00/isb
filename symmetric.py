from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class SymmetricCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        padder = padding.ANSIX923(64).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(
            algorithms.TripleDES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        return iv, encryptor.update(padded_data) + encryptor.finalize()

    def decrypt(self, iv, ciphertext):
        cipher = Cipher(
            algorithms.TripleDES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.ANSIX923(64).unpadder()
        return unpadder.update(decrypted_padded) + unpadder.finalize()