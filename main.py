import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from asymmetric import AsymmetricCipher
from symmetric import SymmetricCipher
from file_manager import FileManager
from crypto_utils import CryptoUtils



class HybridCryptoSystem:
    def __init__(self):
        self.file_manager = FileManager()
        self.settings = self.file_manager.load_settings()
        self.utils = CryptoUtils()

    def generate_keys(self, key_size=192):
        sym_key = self.utils.generate_symmetric_key(key_size)
        private_key, public_key = AsymmetricCipher.generate_keys()
        encrypted_sym_key = AsymmetricCipher.encrypt(public_key, sym_key)

        self.file_manager.save_key(
            self.settings['symmetric_key'],
            self.utils.b64_encode(sym_key)
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
            self.utils.b64_encode(encrypted_sym_key)
        )

    def encrypt_file(self):
        private_key_pem = self.file_manager.load_key(self.settings['secret_key'])
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None,
            backend=default_backend()
        )

        encrypted_sym_key = self.utils.b64_decode(
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
            self.utils.b64_encode(iv + ciphertext)
        )

    def decrypt_file(self):
        private_key_pem = self.file_manager.load_key(self.settings['secret_key'])
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None,
            backend=default_backend()
        )

        encrypted_sym_key = self.utils.b64_decode(
            self.file_manager.load_key(self.settings['encrypted_symmetric_key'])
        )
        sym_key = AsymmetricCipher.decrypt(private_key, encrypted_sym_key)

        cipher = SymmetricCipher(sym_key)
        encrypted_data = self.utils.b64_decode(
            self.file_manager.load_key(self.settings['encrypted_file'])
        )
        iv, ciphertext = encrypted_data[:8], encrypted_data[8:]
        plaintext = cipher.decrypt(iv, ciphertext)

        self.file_manager.save_key(
            self.settings['decrypted_file'],
            plaintext,
            is_binary=True
        )


class ConsoleMenu:
    def __init__(self, crypto_system):
        self.crypto = crypto_system
        self.utils = CryptoUtils()

    def show_menu(self):
        self.utils.clear_screen()
        print("=== Гибридная криптосистема (3DES + RSA) ===")
        print("1. Генерация ключей")
        print("2. Шифрование файла")
        print("3. Дешифрование файла")
        print("4. Выход")
        return input("Выберите действие (1-4): ")

    def show_key_size_menu(self):
        self.utils.clear_screen()
        print("=== Выбор размера ключа 3DES ===")
        print("1. 64 бита (менее безопасно)")
        print("2. 128 бит")
        print("3. 192 бита (наиболее безопасно)")
        choice = input("Выберите размер ключа (1-3): ")
        return {'1': 64, '2': 128, '3': 192}.get(choice, 192)

    def run(self):
        while True:
            choice = self.show_menu()

            if choice == '1':
                key_size = self.show_key_size_menu()
                self.crypto.generate_keys(key_size)
                print("\nКлючи успешно сгенерированы!")
                input("Нажмите Enter для продолжения...")

            elif choice == '2':
                self.crypto.encrypt_file()
                print("\nФайл успешно зашифрован!")
                input("Нажмите Enter для продолжения...")

            elif choice == '3':
                self.crypto.decrypt_file()
                print("\nФайл успешно расшифрован!")
                input("Нажмите Enter для продолжения...")

            elif choice == '4':
                print("Выход из программы...")
                break

            else:
                print("Неверный выбор! Попробуйте снова.")
                input("Нажмите Enter для продолжения...")


if __name__ == '__main__':
    try:
        system = HybridCryptoSystem()
        menu = ConsoleMenu(system)
        menu.run()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")
    except Exception as e:
        print(f"\nПроизошла ошибка: {str(e)}")