import os
import json
from cryptography.hazmat.primitives import padding, serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import b64encode, b64decode


class HybridCryptoSystem:
    def __init__(self):
        self.settings = self.load_settings()

    def load_settings(self):
        '''
        Загрузка настроек из файла settings.json
        :return: словарь с настройками путей к файлам
        '''
        with open('settings.json') as json_file:
            return json.load(json_file)

    def save_settings(self):
        '''
        Сохранение настроек в файл
        '''
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)

    def clear_screen(self):
        '''
        очистка экрана консоли
        '''
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        '''
        Отображение главного меню
        :return: выбранный пользователем пункт меню
        '''
        self.clear_screen()
        print("=== Гибридная криптосистема (3DES + RSA) ===")
        print("1. Генерация ключей")
        print("2. Шифрование файла")
        print("3. Дешифрование файла")
        print("4. Настройки путей")
        print("5. Выход")

        choice = input("Выберите действие (1-5): ")
        return choice

    def show_key_size_menu(self):
        '''
        Меню выбора размера ключа
        :return: выбранный вариант размера ключа
        '''
        self.clear_screen()
        print("=== Выбор размера ключа 3DES ===")
        print("1. 64 бита (менее безопасно)")
        print("2. 128 бит")
        print("3. 192 бита (наиболее безопасно)")

        choice = input("Выберите размер ключа (1-3): ")
        return choice

    def generate_keys(self):
        '''
        Генерация всех необходимых ключей
        '''
        self.clear_screen()
        print("=== Генерация ключей ===")

        choice = self.show_key_size_menu()
        if choice == '1':
            key_size = 64
        elif choice == '2':
            key_size = 128
        else:
            key_size = 192

        symmetric_key = os.urandom(key_size // 8)
        print(f"\nСгенерирован симметричный ключ 3DES ({key_size} бит)")

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        print("Сгенерирована пара ключей RSA (2048 бит)")

        with open(self.settings['public_key'], 'w') as pub_out:
            pub_out.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8'))

        with open(self.settings['secret_key'], 'w') as priv_out:
            priv_out.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8'))

        encrypted_sym_key = public_key.encrypt(
            symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        with open(self.settings['encrypted_symmetric_key'], 'w') as enc_key_out:
            enc_key_out.write(b64encode(encrypted_sym_key).decode('utf-8'))

        with open(self.settings['symmetric_key'], 'w') as sym_out:
            sym_out.write(b64encode(symmetric_key).decode('utf-8'))

        print("\nВсе ключи успешно сохранены в текстовых файлах:")
        print(f"- Публичный ключ: {self.settings['public_key']}")
        print(f"- Приватный ключ: {self.settings['secret_key']}")
        print(f"- Зашифрованный симметричный ключ: {self.settings['encrypted_symmetric_key']}")
        print(f"- Исходный симметричный ключ: {self.settings['symmetric_key']}")

        input("\nНажмите Enter для возврата в меню...")

    def encrypt_file(self):
        '''
        Шифрование файла с помощью гибридной системы
        '''
        self.clear_screen()
        print("=== Шифрование файла ===")

        if not os.path.exists(self.settings['initial_file']):
            print(f"\nОшибка: файл {self.settings['initial_file']} не найден!")
            input("Нажмите Enter для возврата в меню...")
            return

        try:
            with open(self.settings['secret_key'], 'r') as priv_in:
                private_key = serialization.load_pem_private_key(
                    priv_in.read().encode('utf-8'),
                    password=None,
                    backend=default_backend()
                )

            with open(self.settings['encrypted_symmetric_key'], 'r') as enc_key_in:
                encrypted_sym_key = b64decode(enc_key_in.read())

            symmetric_key = private_key.decrypt(
                encrypted_sym_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            with open(self.settings['initial_file'], 'rb') as file_in:
                plaintext = file_in.read()

            padder = padding.ANSIX923(64).padder()
            padded_data = padder.update(plaintext) + padder.finalize()
            iv = os.urandom(8)

            cipher = Cipher(
                algorithms.TripleDES(symmetric_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            with open(self.settings['encrypted_file'], 'w') as file_out:
                file_out.write(b64encode(iv + ciphertext).decode('utf-8'))

            print(f"\nФайл успешно зашифрован и сохранен как {self.settings['encrypted_file']}")

        except Exception as e:
            print(f"\nОшибка при шифровании: {str(e)}")

        input("\nНажмите Enter для возврата в меню...")

    def decrypt_file(self):
        '''
        Дешифрование файла с помощью гибридной системы
        '''
        self.clear_screen()
        print("=== Дешифрование файла ===")

        if not os.path.exists(self.settings['encrypted_file']):
            print(f"\nОшибка: файл {self.settings['encrypted_file']} не найден!")
            input("Нажмите Enter для возврата в меню...")
            return

        try:
            with open(self.settings['secret_key'], 'r') as priv_in:
                private_key = serialization.load_pem_private_key(
                    priv_in.read().encode('utf-8'),
                    password=None,
                    backend=default_backend()
                )

            with open(self.settings['encrypted_symmetric_key'], 'r') as enc_key_in:
                encrypted_sym_key = b64decode(enc_key_in.read())

            symmetric_key = private_key.decrypt(
                encrypted_sym_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            with open(self.settings['encrypted_file'], 'r') as file_in:
                encrypted_data = b64decode(file_in.read())

            iv = encrypted_data[:8]
            ciphertext = encrypted_data[8:]

            cipher = Cipher(
                algorithms.TripleDES(symmetric_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

            unpadder = padding.ANSIX923(64).unpadder()
            decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

            with open(self.settings['decrypted_file'], 'wb') as file_out:
                file_out.write(decrypted_data)

            print(f"\nФайл успешно расшифрован и сохранен как {self.settings['decrypted_file']}")

        except Exception as e:
            print(f"\nОшибка при дешифровании: {str(e)}")

        input("\nНажмите Enter для возврата в меню...")

    def run(self):
        '''
        Основной цикл программы
        '''
        while True:
            choice = self.show_menu()

            if choice == '1':
                self.generate_keys()
            elif choice == '2':
                self.encrypt_file()
            elif choice == '3':
                self.decrypt_file()
            elif choice == '4':
                self.save_settings()
                print("Настройки сохранены!")
                input("Нажмите Enter для продолжения...")
            elif choice == '5':
                print("Выход из программы...")
                break
            else:
                print("Неверный выбор! Попробуйте снова.")
                input("Нажмите Enter для продолжения...")


if __name__ == '__main__':
    try:
        crypto_system = HybridCryptoSystem()
        crypto_system.run()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")