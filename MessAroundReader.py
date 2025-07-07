from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QMenu, QFileDialog, QApplication, QLabel, QSystemTrayIcon
from PySide6.QtCore import Qt, QPoint, Slot, Signal

from file_readers.Resource import Resource, ResourceType
from ui.StyleDialog import StyleDialog
from config.configuration import config
from file_readers.file_reader_factory import file_reader_factory
import typing


class MessAroundReader(QMainWindow):
    __window_style_changed = Signal()
    __contents_changed = Signal()
    __isLeftPressed = False
    __isRightPressed = False
    __dragStart = QPoint(0, 0)
    __windowDragStart = QPoint(0, 0)
    __isForcedToTop = False
    __index = 0

    def __init__(self):
        super().__init__()
        self.__current_reader = None
        self.__content_label = QLabel(self)
        self.__styleDialog = StyleDialog()
        self.init_style_dialog()

        self.__tray_icon = QSystemTrayIcon(self)
        self.set_reader_tray_icon()

        self.init_window_style()
        self.init_signals_and_slots()
        self.show_file_contents()

    def mess_around_show(self):
        self.show()
        self.__tray_icon.show()

    def mousePressEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        if a0.button() == QtCore.Qt.MouseButton.LeftButton:
            self.__isLeftPressed = True
            self.__dragStart = a0.globalPosition().toPoint()
            self.__windowDragStart = self.pos()
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
            config.set_window_pos(self.pos())
        elif a0.button() == Qt.MouseButton.RightButton and self.__isRightPressed:
            self.__isRightPressed = False
            self.show_context_menu(a0.globalPosition().toPoint())

    def mouseDoubleClickEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.hide()

    def wheelEvent(self, a0: typing.Optional[QtGui.QWheelEvent]):
        if self.__current_reader is None:
            return

        lines = len(self.__current_reader.get_parsed_data())

        if a0.angleDelta().y() > 0:
            self.__index = self.__index - 1 if self.__index > 0 else 0
        else:
            self.__index = self.__index + 1 if self.__index < lines - 1 else lines - 1

        self.emit_contents_changed()

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
        action.triggered.connect(lambda: self.quit_app())

    def show_file_contents(self):
        if self.__current_reader is not None:
            parsed_data: list[Resource] = self.__current_reader.get_parsed_data()
            self.refresh_content_label(parsed_data[self.__index])
        else:
            default_resource = Resource(ResourceType.TEXT, '选择一个文件')
            self.refresh_content_label(default_resource)

        self.__content_label.show()

    def refresh_content_label(self, resource: Resource):
        self.__content_label.setText(resource.get_data())
        style_sheet = f"color: {config.get_font_color().name()}; "
        font = config.get_font()
        font.setPointSize(config.get_font_size())
        if resource.get_type() != ResourceType.TEXT:
            font.setBold(True)
            style_sheet += "text-decoration: underline; "
        self.__content_label.setFont(font)
        print(style_sheet)
        self.__content_label.setStyleSheet(style_sheet)
        # self.__content_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.__content_label.adjustSize()

    def select_file(self):
        file_name = QFileDialog.getOpenFileName(self,
                                                '选择文件',
                                                'D:/',
                                                '电子书 (*.txt *.epub *.mobi);;')
        if len(file_name) != 0:
            print(file_name[0])
            self.__current_reader = file_reader_factory.get_file_reader(file_name[0])
            if self.__current_reader is not None:
                self.__current_reader.read_file(file_name[0])
                self.__index = 0
                self.emit_contents_changed()

    def force_to_top(self):
        self.__isForcedToTop = not self.__isForcedToTop
        if self.__isForcedToTop:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()

    def recover_window(self):
        self.show()
        self.activateWindow()

    def quit_app(self):
        QApplication.exit()
        config.save_config()

    def refresh_window_style(self):
        self.setStyleSheet(f"background-color: {config.get_bg_color().name()}")
        self.show()

    def init_window_style(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.resize(400, 20)
        self.setMinimumWidth(200)
        self.setStyleSheet(f"background-color: {config.get_bg_color().name()}")
        self.move(config.get_window_pos())

    def set_reader_tray_icon(self):
        self.__tray_icon.setIcon(QIcon(":/images/reader.ico"))
        self.set_tray_icon_menu()

    def set_tray_icon_menu(self):
        menu = QMenu()
        action = menu.addAction('退出')
        action.triggered.connect(lambda: self.quit_app())
        self.__tray_icon.setContextMenu(menu)

        self.__tray_icon.activated.connect(self.handle_tray_icon_activated)

    def handle_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.recover_window()

    def init_signals_and_slots(self):
        self.__window_style_changed.connect(self.refresh_window_style)
        self.__contents_changed.connect(self.show_file_contents)

    def init_style_dialog(self):
        if self.__styleDialog is not None:
            self.__styleDialog.set_window_style_changed_callback(self.emit_window_style_changed)
            self.__styleDialog.set_contents_changed_callback(self.emit_contents_changed)

    def emit_window_style_changed(self):
        self.__window_style_changed.emit()

    def emit_contents_changed(self):
        self.__contents_changed.emit()
