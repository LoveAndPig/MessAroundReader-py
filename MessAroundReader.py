from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QMenu, QFileDialog
from PyQt6.QtCore import Qt, QPoint, QPointF, pyqtSlot
import typing


class MessAroundReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__isLeftPressed = False
        self.__isRightPressed = False
        self.__dragStart = QPoint(0, 0)
        self.__windowDragStart = QPoint(0, 0)
        self.__isForcedToTop = False

    def mess_around_show(self):
        super().show()

    def mousePressEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        if a0.button() == QtCore.Qt.MouseButton.LeftButton:
            self.__isLeftPressed = True
            self.__dragStart = a0.pos()
            self.__windowDragStart = self.pos()
        elif a0.button() == Qt.MouseButton.RightButton:
            self.__isRightPressed = True

    def mouseMoveEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        if a0.button() == Qt.MouseButton.LeftButton and self.__isLeftPressed:
            current_pos = a0.pos()
            current_win_pos = current_pos - self.__dragStart + self.__windowDragStart
            self.move(current_win_pos)

    def mouseReleaseEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.__isLeftPressed = False
        elif a0.button() == Qt.MouseButton.RightButton:
            self.__isRightPressed = False
            self.show_context_menu(a0.pos())

    def wheelEvent(self, a0: typing.Optional[QtGui.QWheelEvent]) -> None:
        pass

    def show_context_menu(self, pos):
        menu = QMenu(self)
        self.show_file_select_menu(menu)
        self.show_force_to_top_menu(menu)

        menu.exec(pos)

    def show_file_select_menu(self, menu):
        action = menu.addAction('选择文件')
        action.triggered.connect(self.select_file())

    def show_force_to_top_menu(self, menu):
        action = None
        if self.__isForcedToTop:
            action = menu.addAction('取消置顶')
        else:
            action = menu.addAction('置顶')

        self.__isForcedToTop = not self.__isForcedToTop
        action.triggered.connect(self.force_to_top())

    def show_style_edit_menu(self, menu):
        pass

    @pyqtSlot
    def select_file(self):
        # dialog = QFileDialog(self)
        file_name = QFileDialog.getOpenFileName(self,
                                                '选择文件',
                                                'D:/reader/nvl',
                                                '电子书 (*.txt *.epub *.mobi);;')
        if len(file_name) != 0:
            pass

    def force_to_top(self):
        if self.__isForcedToTop:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)

    def init_window_style(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.resize(400, 20)
        self.setMinimumWidth(200)
