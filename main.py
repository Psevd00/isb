from hybrid_crypto import HybridCryptoSystem
from crypto_utils import CryptoUtils


class ConsoleMenu:
    def __init__(self, crypto_system):
        self.crypto = crypto_system

    def show_menu(self):
        print("=== Гибридная криптосистема (3DES + RSA) ===")
        print("1. Генерация ключей")
        print("2. Шифрование файла")
        print("3. Дешифрование файла")
        print("4. Выход")
        return input("Выберите действие (1-4): ")

    def show_key_size_menu(self):
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