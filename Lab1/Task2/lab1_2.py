import json

from collections import Counter

from constants2 import *


def load_key(file_path):
    """Загружает ключ замены из JSON файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file) 
    except Exception as e:
        raise Exception(f"Error")


def load_cipher_text(file_path):
    """
    Читает содержимое текстового файла по указанному пути.
    :param file_path: Путь к файлу
    :return: Содержимое файла в виде строки
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error")


def load_russian_frequencies(file_path):
    """
    Загружает частоты появления букв русского алфавита.
    :param file_path: Путь к файлу
    :return: Словарь с частотами появления букв
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        raise Exception(f"Error")


def analyze_frequency(text):
    """
    Анализирует частоту появления каждого символа в тексте.
    :param text: Исходный текст
    :return: Словарь с частотами появления символов
    """
    try:
        if not text:
            raise ValueError("Текст не может быть пустым")
        freq_counter = Counter(text)
        total_chars = sum(freq_counter.values())
        return {char: count / total_chars for char, count in freq_counter.items()}
    except Exception as e:
        raise Exception(f"Error")


def decrypt_with_key(ciphertext, key):
    """
    Расшифровывает текст с использованием созданного сопоставления.
    :param ciphertext: Зашифрованный текст
    :param key: Таблица замены символов
    :return: Расшифрованный текст
    """
    try:
        decrypted = []
        for char in ciphertext:
            decrypted.append(key.get(char, char))
        return ''.join(decrypted)
    except Exception as e:
        raise Exception(f"Error")


def save_json(data, file_path):
    """
    Сохраняет данные в формате JSON.
    :param data: Данные для сохранения
    :param file_path: Путь к файлу
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_text(data, file_path):
    """
    Сохраняет текстовые данные в файл.
    :param data: Текст для сохранения
    :param file_path: Путь к файлу
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)


def main():
    try:
        key = load_key(KEY_PATH)
        cipher_text = load_cipher_text(CIPHER_TEXT_PATH)
        decrypted_text = decrypt_with_key(cipher_text, key)
        save_text(decrypted_text, DECRYPTED_TEXT_OUTPUT)

        russian_frequencies = load_russian_frequencies(RUSSIAN_FREQUENCIES_PATH)
        cipher_frequencies = analyze_frequency(decrypted_text)

        cipher_frequencies_sorted = dict(
            sorted(cipher_frequencies.items(), key=lambda item: (-item[1], item[0]))
        )
        save_json(cipher_frequencies_sorted, CIPHER_FREQUENCIES_OUTPUT)

        print(f"Расшифровка завершена. Созданы файлы: {DECRYPTED_TEXT_OUTPUT}")

    except Exception as e:
        print(f"Ошибка: {str(e)}")


if __name__ == "__main__":
    main()
