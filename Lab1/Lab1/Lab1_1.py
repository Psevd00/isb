import json
import os
import random


def generate_key(alphabet):
    """
    Генерация случайного ключа на основе алфавита.
    :param alphabet: Строка с алфавитом
    :return: Словарь, где ключ — символ алфавита, значение — случайный символ
    """
    shuffled_alphabet = list(alphabet)
    random.shuffle(shuffled_alphabet)
    return {original: shuffled for original, shuffled in zip(alphabet, shuffled_alphabet)}


def encrypt(text, key):
    """
    Шифрование текста с использованием ключа (игнорирует символы, не входящие в алфавит).
    :param text: Исходный текст
    :param key: Словарь с ключом шифрования
    :return: Зашифрованный текст
    """
    return ''.join([key[char] if char in key else char for char in text])


def save_encrypted_text(text, file_path):
    """
    Сохранение зашифрованного текста в файл.
    :param text: Зашифрованный текст
    :param file_path: Путь к файлу для сохранения
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


def save_key(key, file_path):
    """
    Сохранение ключа в файл в формате JSON.
    :param key: Словарь с ключом шифрования
    :param file_path: Путь к файлу для сохранения
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(key, file, ensure_ascii=False, indent=4)


def main():
    """
    Основная функция для запуска программы.
    """
    # Определяем алфавит
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '

    # Определяем пути к файлам
    task_directory = os.path.join('Task1')
    input_file = os.path.join(task_directory, 'original_text.txt')
    encrypted_file = os.path.join(task_directory, 'encrypted_text.txt')
    key_file = os.path.join(task_directory, 'key.json')

    # Чтение исходного текста
    with open(input_file, 'r', encoding='utf-8') as file:
        original_text = file.read().upper()

    # Генерация ключа
    key = generate_key(alphabet)

    # Шифрование текста
    encrypted_text = encrypt(original_text, key)

    # Сохранение зашифрованного текста и ключа
    save_encrypted_text(encrypted_text, encrypted_file)
    save_key(key, key_file)

    print("Текст успешно зашифрован и сохранен.")


if __name__ == "__main__":
    main()