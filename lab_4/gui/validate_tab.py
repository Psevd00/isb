from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from backend.luhn_validator import LuhnValidator

class ValidateTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        form = QFormLayout()

        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("Введите номер карты для проверки")
        form.addRow("Номер карты:", self.card_input)

        self.check_button = QPushButton("Проверить по алгоритму Луна")
        self.check_button.clicked.connect(self.check_card)

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        font = self.result_label.font()
        font.setPointSize(12)
        self.result_label.setFont(font)

        self.layout.addLayout(form)
        self.layout.addWidget(self.check_button)
        self.layout.addWidget(self.result_label)

    def check_card(self):
        card_number = self.card_input.text().strip()
        if not card_number or not card_number.isdigit():
            QMessageBox.warning(self, "Ошибка ввода", "Введите корректный номер карты (только цифры).")
            return

        valid = LuhnValidator.validate(card_number)
        if valid:
            self.result_label.setText("Номер карты корректен по алгоритму Луна.")
            self.result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.result_label.setText("Номер карты некорректен по алгоритму Луна.")
            self.result_label.setStyleSheet("color: red; font-weight: bold;")
