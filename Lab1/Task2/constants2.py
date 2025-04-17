import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CIPHER_FREQUENCIES_OUTPUT = os.path.join(BASE_DIR, "cipher_frequencies.json")
CIPHER_TEXT_PATH = os.path.join(BASE_DIR, "cod4.txt")
DECRYPTED_TEXT_OUTPUT = os.path.join(BASE_DIR, "cod4_decrypted.txt")
KEY_PATH = os.path.join(BASE_DIR, "Key.json")
RUSSIAN_FREQUENCIES_PATH = os.path.join(BASE_DIR, "russian_letter_frequency.json")

