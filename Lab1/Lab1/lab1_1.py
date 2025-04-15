import json
import os
import random

from constants import ALPHABET, ENCRYPTED_FILE, INPUT_FILE, KEY_FILE, TASK_DIRECTORY


def read_file(file_path):
    """
    Читает содержимое текстового файла по указанному пути.
    :param file_path: Путь к файлу
    :return: Содержимое файла в виде строки
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise Exception(f"Файл не найден: {file_path}")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {str(e)}")

def generate_key(alphabet):
    """
    Генерация случайного ключа на основе алфавита.
    :param alphabet: Строка с алфавитом
    :return: Словарь, где ключ — символ алфавита, значение — случайный символ
    """
    try:
        if not alphabet:
            raise ValueError("Алфавит не может быть пустым")

        shuffled_alphabet = list(alphabet)
        random.shuffle(shuffled_alphabet)
        return {original: shuffled for original, shuffled in zip(alphabet, shuffled_alphabet)}
    except Exception as e:
        raise Exception(f"ERROR")

def encrypt(text, key):
    """
    Шифрование текста с использованием ключа (игнорирует символы, не входящие в алфавит).
    :param text: Исходный текст
    :param key: Словарь с ключом шифрования
    :return: Зашифрованный текст
    """
    try:
        if not text:
            raise ValueError("Текст не может быть пустым")
        if not key:
            raise ValueError("Ключ не может быть пустым")

        return ''.join([key[char] if char in key else char for char in text])
    except Exception as e:
        raise Exception(f"ERROR")


def save_encrypted_text(text, file_path):
    """
    Сохранение зашифрованного текста в файл.
    :param text: Зашифрованный текст
    :param file_path: Путь к файлу для сохранения
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        raise Exception(f"ERROR")


def save_key(key, file_path):
    """
    Сохранение ключа в файл в формате JSON.
    :param key: Словарь с ключом шифрования
    :param file_path: Путь к файлу для сохранения
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(key, file, ensure_ascii=False, indent=4)
    except Exception as e:
        raise Exception(f"ERROR")


def main():
    """
    Основная функция для запуска программы.
    """
    input_file_path = os.path.join(TASK_DIRECTORY, INPUT_FILE)
    with open(input_file_path, 'r', encoding='utf-8') as file:
        original_text = file.read().upper()

    key = generate_key(ALPHABET)

    encrypted_text = encrypt(original_text, key)

    encrypted_file_path = os.path.join(TASK_DIRECTORY, ENCRYPTED_FILE)
    save_encrypted_text(encrypted_text, encrypted_file_path)

    key_file_path = os.path.join(TASK_DIRECTORY, KEY_FILE)
    save_key(key, key_file_path)

    print("Текст успешно зашифрован и сохранен.")


if __name__ == "__main__":
    main()
