from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QProgressBar)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from backend.benchmark_runner import BenchmarkRunner
import matplotlib.pyplot as plt
import tempfile
import os

class BenchmarkTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        form = QFormLayout()

        self.hash_input = QLineEdit()
        form.addRow("Хеш номера карты (sha1):", self.hash_input)

        self.bin_input = QLineEdit()
        self.bin_input.setPlaceholderText("Пример: 220220, можно несколько через запятую")
        form.addRow("БИН (6 цифр):", self.bin_input)

        self.last4_input = QLineEdit()
        self.last4_input.setMaxLength(4)
        form.addRow("Последние 4 цифры карты:", self.last4_input)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        self.benchmark_button = QPushButton("Запустить замер")
        self.benchmark_button.clicked.connect(self.start_benchmark)

        self.graph_label = QLabel()
        self.graph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Здесь используется Qt
        self.graph_label.setMinimumHeight(300)

        self.layout.addLayout(form)
        self.layout.addWidget(self.benchmark_button)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.graph_label)

        self.benchmark_thread = None

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_finished(self, data):
        process_counts, times, min_proc, min_time = data
        self.progress_bar.setVisible(False)
        self.benchmark_button.setEnabled(True)
        self.plot_graph(process_counts, times, min_proc, min_time)

    def plot_graph(self, x, y, min_proc, min_time):
        plt.figure(figsize=(8, 3), dpi=100)
        plt.plot(x, y, marker='o', color='royalblue')
        plt.title("Время поиска коллизии в зависимости от числа процессов")
        plt.xlabel("Количество процессов")
        plt.ylabel("Время (сек)")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.scatter(min_proc, min_time, color='red', zorder=5)
        plt.annotate(f'Минимум\n{min_proc} процессов\n{min_time:.2f} сек',
                     (min_proc, min_time),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center',
                     fontsize=10,
                     color='darkred')
        # Сохраняем график во временный файл
        tmpfile = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(tmpfile.name)
        plt.close()
        # Загружаем изображение в QLabel
        pixmap = QPixmap(tmpfile.name)
        self.graph_label.setPixmap(pixmap.scaled(
            self.graph_label.width(), self.graph_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        tmpfile.close()
        os.unlink(tmpfile.name)

    def start_benchmark(self):
        target_hash = self.hash_input.text().strip()
        bin_codes = [b.strip() for b in self.bin_input.text().split(",") if b.strip()]
        last_four = self.last4_input.text().strip()
        if not target_hash or not bin_codes or len(last_four) != 4:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
            return

        self.benchmark_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.benchmark_thread = BenchmarkThread(target_hash, last_four, bin_codes)
        self.benchmark_thread.progress.connect(self.update_progress)
        self.benchmark_thread.finished.connect(self.on_finished)
        self.benchmark_thread.start()
