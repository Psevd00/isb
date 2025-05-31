import hashlib
import multiprocessing as mp

from .Operations import write_json


class FindCard:

    @staticmethod
    def hashing_num(num: str) -> str:
        """
        Хэширует указанную строку.
        :param num: номер карты
        :return: полученный хэш
        """
        return hashlib.sha1(num.encode()).hexdigest()

    @staticmethod
    def number_of_cores() -> int:
        """
        Определяет доступное количество процессов.
        :return: количество процессов
        """
        return mp.cpu_count()

    @staticmethod
    def find_card_parallel(bins: list[str], last_digits: str, target_hash: str, cores: int) -> str:
        """
        Поиск подходящего номера карты с помощью многопроцессорной обработки.
        :return: номер найденной карточки
        """
        total_range = 10**6
        chunk_size = total_range // cores

        with mp.Pool(processes=cores) as pool:
            results = []
            for bin in bins:
                for i in range(cores):
                    start = i * chunk_size
                    end = start + chunk_size if i != cores - 1 else total_range
                    results.append(
                        pool.apply_async(
                            FindCard.generate_cards_hash,
                            (bin, last_digits, start, end, target_hash),
                        )
                    )
            for result in results:
                found = result.get()
                if found:
                    pool.terminate()
                    return found[0]

        return None

    @staticmethod
    def generate_cards_hash(bin: str, last_digits: str, start: int, end: int, hash: str) -> tuple[str, str]:
        """
        Генерация номера карт в указанном диапазоне.
        :return: рандомный хэш
        """
        for middle in range(start, end):
            card = f"{bin}{middle:06}{last_digits}"
            rand_hash = FindCard.hashing_num(card)
            if rand_hash == hash:
                return card, rand_hash
        return None

    @staticmethod
    def serialization_res(bins: list[str], last_digits: str, target_hash: str, cores: int, filepath: str) -> None:
        """
        Сериализует номер найденной карточки.
        """
        try:
            res = FindCard.find_card_parallel(bins, last_digits, target_hash, cores)
            write_json(filepath, {"card_number": res})
        except Exception as exc:
            raise Exception(f"Error serializing private key: {exc}")
