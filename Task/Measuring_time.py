import time
import matplotlib.pyplot as plt


class PerformanceMeasurer:
    def meas_time(self, bins: list[str], last_digits: str, target_hash: str) -> list[tuple[int, float]]:
        num_cores = CardFinder.number_of_cores()
        max_processes = int(num_cores * 1.5)
        time_results = []

        for processes in range(1, max_processes + 1):
            start_time = time.time()
            CardFinder().find_card_parallel(bins, last_digits, target_hash, processes)
            execution_time = time.time() - start_time
            time_results.append((processes, execution_time))
            print(f"Процессы: {processes}, Время: {execution_time:.2f} сек")

        return time_results

    def _format_table(self, data: list[tuple[int, float]]) -> str:
        headers = ["Процессы", "Время (сек)"]
        col_width = max(len(str(x)) for row in data for x in row) + 2
        header_width = max(len(h) for h in headers) + 2

        table = f"{headers[0]:<{header_width}} {headers[1]:<{col_width}}\n"
        table += "-" * (header_width + col_width) + "\n"

        for processes, exec_time in data:
            table += f"{processes:<{header_width}} {exec_time:<{col_width}.4f}\n"

        return table

    def print_time_results(self, time_res: list[tuple[int, float]]) -> None:
        if not time_res:
            print("Нет данных для отображения")
            return

        best_result = min(time_res, key=lambda x: x[1])
        print("\nРезультаты измерений времени:")
        print(self._format_table(time_res))
        print(f"Лучший результат: {best_result[0]} процессов, {best_result[1]:.4f} сек")

        with open("time_results.txt", "w", encoding="utf-8") as f:
            f.write("Результаты измерений времени:\n")
            f.write(self._format_table(time_res))
            f.write(f"\nЛучший результат: {best_result[0]} процессов, {best_result[1]:.4f} сек")

    def plot_time(self, time_res: list[tuple[int, float]]) -> None:
        if not time_res:
            print("Нет данных для построения графика")
            return

        processes = [x[0] for x in time_res]
        times = [x[1] for x in time_res]
        best_idx = times.index(min(times))

        plt.figure(figsize=(10, 6))
        plt.plot(processes, times, 'bo-', label='Время выполнения')
        plt.plot(processes[best_idx], times[best_idx], 'ro', label='Лучший результат')

        plt.title('Зависимость времени выполнения от количества процессов')
        plt.xlabel('Количество процессов')
        plt.ylabel('Время (секунды)')
        plt.grid(True)
        plt.xticks(processes)
        plt.legend()

        plt.tight_layout()
        plt.savefig('performance_graph.png')
        print("\nГрафик сохранен в файл 'performance_graph.png'")
        plt.show()
