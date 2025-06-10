import sys
import multiprocessing as mp
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    mp.freeze_support()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
