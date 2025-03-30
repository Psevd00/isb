import json

from collections import Counter

from constants2 import *


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
        raise Exception(f"ERROR")

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
        raise Exception(f"ERROR")


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
        raise Exception(f"ERROR")


def create_mapping(cipher_freq, russian_freq):
    """
    Создаёт сопоставление между символами зашифрованного текста и русского алфавита.
    :param cipher_freq: Частота появления символов в тексте
    :param russian_freq: Частота появления русских букв
    :return: Таблица замены символов
    """
    try:
        if not cipher_freq or not russian_freq:
            raise ValueError("Частоты символов не могут быть пустыми")

        sorted_cipher = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
        sorted_russian = sorted(russian_freq.items(), key=lambda x: x[1], reverse=True)

        mapping = {}
        for (cipher_char, _), (russian_char, _) in zip(sorted_cipher, sorted_russian):
            if cipher_char not in mapping.values():
                mapping[cipher_char] = russian_char
        return mapping
    except Exception as e:
        raise Exception(f"ERROR")


def decrypt_text(text, mapping):
    """
    Расшифровывает текст с использованием созданного сопоставления.
    :param text: Зашифрованный текст
    :param mapping: Таблица замены символов
    :return: Расшифрованный текст
    """
    try:
        if not text:
            raise ValueError("Текст не может быть пустым")
        if not mapping:
            raise ValueError("Таблица замены не может быть пустой")

        return ''.join(mapping.get(char, char) for char in text)
    except Exception as e:
        raise Exception(f"ERROR")


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
    cipher_text = load_cipher_text(CIPHER_TEXT_PATH)
    russian_frequencies = load_russian_frequencies(RUSSIAN_FREQUENCIES_PATH)

    cipher_frequencies = analyze_frequency(cipher_text)

    cipher_frequencies_sorted = dict(
        sorted(cipher_frequencies.items(), key=lambda item: (-item[1], item[0]))
    )
    save_json(cipher_frequencies_sorted, CIPHER_FREQUENCIES_OUTPUT)

    mapping = create_mapping(cipher_frequencies, russian_frequencies)
    decrypted_text = decrypt_text(cipher_text, mapping)

    save_json(mapping, MAPPING_OUTPUT)
    save_text(decrypted_text, DECRYPTED_TEXT_OUTPUT)

    print(f"Расшифровка завершена. Файлы: {DECRYPTED_TEXT_OUTPUT}, {MAPPING_OUTPUT}, "
          f"{CIPHER_FREQUENCIES_OUTPUT}")


if __name__ == "__main__":
    main()
