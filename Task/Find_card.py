import hashlib
import multiprocessing as mp
from .Operations import JsonOperations


class CardFinder:
    @staticmethod
    def hashing_num(num: str) -> str:
        return hashlib.sha1(num.encode()).hexdigest()

    @staticmethod
    def number_of_cores() -> int:
        return mp.cpu_count()

    def find_card_parallel(self, bins: list[str], last_digits: str, target_hash: str, cores: int = None) -> str:
        cores = cores or self.number_of_cores()
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
                            self.generate_cards_hash,
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
        for middle in range(start, end):
            card = f"{bin}{middle:06}{last_digits}"
            rand_hash = CardFinder.hashing_num(card)
            if rand_hash == hash:
                return card, rand_hash
        return None

    def serialization_res(self, bins: list[str], last_digits: str, target_hash: str, filepath: str) -> None:
        try:
            res = self.find_card_parallel(bins, last_digits, target_hash)
            JsonOperations.write(filepath, {"card_number": res})
        except Exception as exc:
            raise Exception(f"Error serializing private key: {exc}")
