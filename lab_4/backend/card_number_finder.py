import hashlib
import multiprocessing as mp
from typing import Optional

class CardNumberFinder:
    def __init__(self, target_hash: str, last_four: str, bin_codes, hash_algorithm: str = "sha1"):
        self.target_hash = target_hash.lower()
        self.last_four = last_four
        self.bin_codes = bin_codes if isinstance(bin_codes, list) else [bin_codes]
        self.hash_algorithm = hash_algorithm

    def _hash_card_number(self, card_number: str) -> str:
        h = hashlib.new(self.hash_algorithm)
        h.update(card_number.encode())
        return h.hexdigest()

    def _search_range(self, bin_code: str, start: int, end: int) -> Optional[str]:
        for middle_number in range(start, end):
            middle_str = f"{middle_number:06d}"
            card_number = f"{bin_code}{middle_str}{self.last_four}"
            if self._hash_card_number(card_number) == self.target_hash:
                return card_number
        return None

    def _worker(self, args):
        bin_code, start, end = args
        return self._search_range(bin_code, start, end)

    def find_card(self, processes: int = None) -> Optional[str]:
        if processes is None:
            processes = mp.cpu_count()

        RANGE_SIZE = 1_000_000
        jobs = []
        for bin_code in self.bin_codes:
            step = RANGE_SIZE // processes
            for i in range(processes):
                start = i * step
                end = (i + 1) * step if i != processes - 1 else RANGE_SIZE
                jobs.append((bin_code, start, end))

        with mp.Pool(processes=processes) as pool:
            for result in pool.imap_unordered(self._worker, jobs):
                if result is not None:
                    pool.terminate()
                    return result
        return None
