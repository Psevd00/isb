import time
from .card_number_finder import CardNumberFinder

class BenchmarkRunner:
    def __init__(self, target_hash: str, last_four: str, bin_codes, hash_algorithm: str = "sha1"):
        self.target_hash = target_hash
        self.last_four = last_four
        self.bin_codes = bin_codes if isinstance(bin_codes, list) else [bin_codes]
        self.hash_algorithm = hash_algorithm

    def _run_trial(self, num_processes: int) -> float:
        finder = CardNumberFinder(self.target_hash, self.last_four, self.bin_codes, self.hash_algorithm)
        start_time = time.perf_counter()
        finder.find_card(processes=num_processes)
        end_time = time.perf_counter()
        return end_time - start_time

    def run_benchmark(self, update_progress_callback=None):
        max_process_count = max(1, int(mp.cpu_count() * 1.5))
        process_counts = list(range(1, max_process_count + 1))
        times = []
        for idx, proc in enumerate(process_counts):
            elapsed = self._run_trial(proc)
            times.append(elapsed)
            if update_progress_callback:
                update_progress_callback(idx + 1, len(process_counts))
        min_time = min(times)
        min_proc = process_counts[times.index(min_time)]
        return process_counts, times, min_proc, min_time
