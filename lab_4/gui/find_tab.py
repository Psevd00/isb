import json
import multiprocessing as mp

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton,
    QProgressBar, QTextEdit, QFileDialog, QMessageBox, QHBoxLayout
)


class FindTab(QWidget):
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

        self.proc_label = QLabel(f"Доступно ядер: {mp.cpu_count()}")
        form.addRow("", self.proc_label)

        self.find_button = QPushButton("Начать подбор")
        self.find_button.clicked.connect(self.start_find)

        self.outfile_button = QPushButton("Выбрать файл для сохранения")
        self.outfile_button.clicked.connect(self.browse_outfile)
        self.outfile_path = QLabel("Результат будет сохранён в: found_card.json")
        self.outfile_path.setWordWrap(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(80)

        self.layout.addLayout(form)
        hbox = QHBoxLayout()  # Здесь используется QHBoxLayout
        hbox.addWidget(self.find_button)
        hbox.addWidget(self.outfile_button)
        self.layout.addLayout(hbox)
        self.layout.addWidget(self.outfile_path)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(QLabel("Результат:"))
        self.layout.addWidget(self.result_text)

        self.find_thread = None
        self.current_outfile = "found_card.json"

    def browse_outfile(self):
        path, _ = QFileDialog.getSaveFileName(self, "Выбор файла для сохранения", "found_card.json", "JSON Files (*.json);;All Files (*)")
        if path:
            self.current_outfile = path
            self.outfile_path.setText(f"Результат будет сохранён в: {self.current_outfile}")

    def start_find(self):
        target_hash = self.hash_input.text().strip()
        bin_codes = [b.strip() for b in self.bin_input.text().split(",") if b.strip()]
        last_four = self.last4_input.text().strip()
        if not target_hash or not bin_codes or len(last_four) != 4:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля корректно.")
            return

        self.find_button.setEnabled(False)
        self.result_text.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress

        self.find_thread = FindThread(target_hash, last_four, bin_codes, processes=mp.cpu_count())
        self.find_thread.found.connect(self.on_found)
        self.find_thread.finished.connect(self.on_finished)
        self.find_thread.start()

    def on_found(self, card_number):
        self.result_text.append(f"Найден номер карты: {card_number}")
        try:
            with open(self.current_outfile, "w", encoding="utf-8") as f:
                json.dump({"card_number": card_number}, f, ensure_ascii=False, indent=4)
            self.result_text.append(f"Результат сохранён в {self.current_outfile}")
        except Exception as e:
            self.result_text.append(f"Ошибка при сохранении файла: {e}")

    def on_finished(self):
        self.find_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        if self.result_text.toPlainText().strip() == "":
            self.result_text.append("Карта не найдена.")
