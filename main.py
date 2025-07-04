from MessAroundReader import MessAroundReader
import sys

from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MessAroundReader()
    window.mess_around_show()
    sys.exit(app.exec())


