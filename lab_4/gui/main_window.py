from PyQt6.QtWidgets import QMainWindow, QTabWidget
from gui.find_tab import FindTab
from gui.validate_tab import ValidateTab
from gui.benchmark_tab import BenchmarkTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №4 — Поиск коллизии хеш-функции")
        self.resize(900, 700)
        self.setMinimumSize(720, 600)

        tabs = QTabWidget()
        tabs.addTab(FindTab(), "Подбор номера карты")
        tabs.addTab(ValidateTab(), "Проверка номера карты")
        tabs.addTab(BenchmarkTab(), "Замер времени")

        self.setCentralWidget(tabs)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 14px;
                background-color: #ffffff;
                color: #374151;
            }
            QLabel {
                color: #6b7280;
                font-size: 15px;
            }
            QLineEdit, QTextEdit {
                border: 1.5px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 8px;
                font-size: 15px;
                color: #111827;
            }
            QPushButton {
                background-color: #111827;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-weight: 700;
                letter-spacing: 0.02em;
                min-width: 140px;
                transition: background-color 0.25s ease;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:disabled {
                background-color: #9ca3af;
                color: #4b5563;
            }
            QProgressBar {
                border-radius: 6px;
                border: 1px solid #d1d5db;
                text-align: center;
                font-weight: 600;
            }
            QProgressBar::chunk {
                background-color: #2563eb;
                border-radius: 6px;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #f9fafb;
                color: #374151;
                padding: 12px 25px;
                border-radius: 8px 8px 0 0;
                margin;
            }""")