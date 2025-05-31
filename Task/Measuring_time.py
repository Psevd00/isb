import time

from .Find_card import FindCard



class MeasuringTime:
    @staticmethod
    def meas_time(
            bins: list[str],
            last_digits: str,
            target_hash: str
    ) -> list[tuple[int, float]]:
        """
        Измеряет время поиска коллизии хеша для разного количества процессов
        :param bins: бины карт
        :param last_digits: последние 4 цифры
        :param target_hash: целевой хеш
        :return: список кортежей (количество процессов, время выполнения)
        """
        num_cores = FindCard.number_of_cores()
        max_processes = int(num_cores * 1.5)
        time_results = []

        for processes in range(1, max_processes + 1):
            start_time = time.time()
            FindCard.find_card_parallel(bins, last_digits, target_hash, processes)
            execution_time = time.time() - start_time
            time_results.append((processes, execution_time))
            print(f"Процессы: {processes}, Время: {execution_time:.2f} сек")

        return time_results

    @staticmethod
    def _format_table(data: list[tuple[int, float]]) -> str:
        """Форматирует данные в виде таблицы"""
        headers = ["Процессы", "Время (сек)"]
        col_width = max(len(str(x)) for row in data for x in row) + 2
        header_width = max(len(h) for h in headers) + 2

        # Создаем строку с заголовками
        table = f"{headers[0]:<{header_width}} {headers[1]:<{col_width}}\n"
        table += "-" * (header_width + col_width) + "\n"

        # Добавляем данные
        for processes, exec_time in data:
            table += f"{processes:<{header_width}} {exec_time:<{col_width}.4f}\n"

        return table

    @staticmethod
    def print_time_results(time_res: list[tuple[int, float]]) -> None:
        """
        Выводит результаты измерений в виде таблицы
        :param time_res: результаты измерений
        """
        if not time_res:
            print("Нет данных для отображения")
            return

        best_result = min(time_res, key=lambda x: x[1])

        print("\nРезультаты измерений времени:")
        print(MeasuringTime._format_table(time_res))
        print(f"Лучший результат: {best_result[0]} процессов, {best_result[1]:.4f} сек")

        # Сохраняем в файл
        with open("time_results.txt", "w", encoding="utf-8") as f:
            f.write("Результаты измерений времени:\n")
            f.write(MeasuringTime._format_table(time_res))
            f.write(f"\nЛучший результат: {best_result[0]} процессов, {best_result[1]:.4f} сек")

    @staticmethod
    def plot_time(time_res: list[tuple[int, float]]) -> None:
        """
        Альтернатива графику - вывод таблицы с результатами
        :param time_res: результаты измерений
        """
        MeasuringTime.print_time_results(time_res)