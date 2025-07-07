from PySide6.QtGui import QIcon

from MessAroundReader import MessAroundReader
import sys

from PySide6.QtWidgets import QApplication

from resources.resources_rc import qInitResources


def set_application_icon(reader_app):
    reader_app.setWindowIcon(QIcon(":/images/reader.ico"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qInitResources()
    set_application_icon(app)
    window = MessAroundReader()
    window.mess_around_show()
    app.exec()
