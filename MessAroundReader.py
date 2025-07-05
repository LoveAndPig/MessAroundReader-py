from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QMenu, QFileDialog, QApplication
from PyQt6.QtCore import Qt, QPoint, pyqtSlot
from ui.StyleDialog import StyleDialog
from config.configuration import config
import typing


class MessAroundReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__isLeftPressed = False
        self.__isRightPressed = False
        self.__dragStart = QPoint(0, 0)
        self.__windowDragStart = QPoint(0, 0)
        self.__isForcedToTop = False
        self.__styleDialog = StyleDialog()

        self.init_window_style()

    def mess_around_show(self):
        self.show()

    def mousePressEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        if a0.button() == QtCore.Qt.MouseButton.LeftButton:
            self.__isLeftPressed = True
            self.__dragStart = a0.globalPosition().toPoint()
            self.__windowDragStart = self.pos()
            print(f"drag start x {self.__dragStart.x()}, "
                  f"drag start y {self.__dragStart.y()}, "
                  f"window start x {self.__windowDragStart.x()}, "
                  f"window start y {self.__windowDragStart.y()}")
        elif a0.button() == Qt.MouseButton.RightButton:
            self.__isRightPressed = True

    def mouseMoveEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        if self.__isLeftPressed:
            current_pos = a0.globalPosition().toPoint()
            current_win_pos = current_pos - self.__dragStart + self.__windowDragStart
            self.window().move(current_win_pos)

    def mouseReleaseEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        if a0.button() == Qt.MouseButton.LeftButton and self.__isLeftPressed:
            self.__isLeftPressed = False
        elif a0.button() == Qt.MouseButton.RightButton and self.__isRightPressed:
            self.__isRightPressed = False
            self.show_context_menu(a0.globalPosition().toPoint())

    def wheelEvent(self, a0: typing.Optional[QtGui.QWheelEvent]) -> None:
        pass

    def show_context_menu(self, pos):
        menu = QMenu()
        self.show_file_select_menu(menu)
        self.show_force_to_top_menu(menu)
        self.show_style_edit_menu(menu)
        menu.addSeparator()
        self.show_exit_menu(menu)
        menu.exec(pos)

    def show_file_select_menu(self, menu):
        action = menu.addAction('选择文件')
        action.triggered.connect(lambda: self.select_file())

    def show_force_to_top_menu(self, menu):
        # action = None
        if self.__isForcedToTop:
            action = menu.addAction('取消置顶')
        else:
            action = menu.addAction('置顶')
        action.triggered.connect(lambda: self.force_to_top())

    def show_style_edit_menu(self, menu):
        action = menu.addAction('样式设置')
        action.triggered.connect(lambda: self.__styleDialog.exec())

    def show_exit_menu(self, menu):
        action = menu.addAction('退出')
        action.triggered.connect(lambda: QApplication.exit())

    # @pyqtSlot
    def select_file(self):
        file_name = QFileDialog.getOpenFileName(self,
                                                '选择文件',
                                                'D:/',
                                                '电子书 (*.txt *.epub *.mobi);;')
        if len(file_name) != 0:
            print(file_name[0])

    def force_to_top(self):
        self.__isForcedToTop = not self.__isForcedToTop
        if self.__isForcedToTop:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()

    def init_window_style(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.resize(400, 20)
        self.setMinimumWidth(200)
        self.setStyleSheet(f"background-color: {config.get_bg_color().name()}")
        self.move(config.get_window_pos())

    def init_style_dialog(self):
        pass
