import typing

from PySide6 import QtGui
from PySide6.QtCore import Qt, QPoint, Signal, QSize
from PySide6.QtGui import QIcon, QKeyEvent
from PySide6.QtWidgets import QMainWindow, QMenu, QFileDialog, QApplication, QLabel, QSystemTrayIcon

from config.configuration import config
from constants import PressPurpose
from file_readers.Resource import Resource, ResourceType
from file_readers.file_reader_factory import file_reader_factory
from ui.ChapterDialog import ChapterDialog
from ui.StyleDialog import StyleDialog


class MessAroundReader(QMainWindow):
    __window_style_changed = Signal()
    __contents_changed = Signal()

    def __init__(self):
        super().__init__()
        self.__current_reader = None
        self.__index = 0

        self.__isForcedToTop = False
        self.__resize_threshold = 10
        self.__dragStart = QPoint(0, 0)
        self.__windowDragStart = QPoint(0, 0)
        self.__origin_size = QSize(0, 0)
        self.__press_purpose = PressPurpose.NONE
        self.__content_label = QLabel(self)

        self.__styleDialog = StyleDialog()
        self.init_style_dialog()

        self.__chapter_dialog = ChapterDialog()
        self.init_chapter_dialog()

        self.__tray_icon = QSystemTrayIcon(self)
        self.set_reader_tray_icon()

        self.init_window_style()
        self.init_signals_and_slots()
        self.show_file_contents()

    def mess_around_show(self):
        self.show()
        self.__tray_icon.show()

    def mousePressEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        self.update_press_purpose(event)
        if self.__press_purpose == PressPurpose.MOVE:
            self.__dragStart = event.globalPosition().toPoint()
            self.__windowDragStart = self.pos()
        elif self.__press_purpose == PressPurpose.RESIZE:
            self.__dragStart = event.globalPosition().toPoint()
            self.__origin_size = self.size()
            self.setCursor(Qt.CursorShape.SizeHorCursor)

    def mouseMoveEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        if self.__press_purpose == PressPurpose.MOVE:
            current_pos = event.globalPosition().toPoint()
            current_win_pos = current_pos - self.__dragStart + self.__windowDragStart
            self.window().move(current_win_pos)
        elif self.__press_purpose == PressPurpose.RESIZE:
            current_pos = event.globalPosition().toPoint()
            new_window_width = current_pos.x() - self.__dragStart.x() + self.__origin_size.width()
            self.resize(new_window_width, self.size().height())

    def mouseReleaseEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        if self.__press_purpose == PressPurpose.MOVE:
            config.set_window_pos(self.pos())
        elif self.__press_purpose == PressPurpose.RESIZE:
            config.set_window_width(self.size().width())
        elif self.__press_purpose == PressPurpose.CONTEXT_MENU:
            self.show_context_menu(event.globalPosition().toPoint())
        self.clear_press_purpose()
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseDoubleClickEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.hide()

    def update_press_purpose(self, event: typing.Optional[QtGui.QMouseEvent]):
        if event is None:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            if abs(mouse_pos.x() - self.size().width()) <= self.__resize_threshold:
                self.__press_purpose = PressPurpose.RESIZE
            else:
                self.__press_purpose = PressPurpose.MOVE
        elif event.button() == Qt.MouseButton.RightButton:
            self.__press_purpose = PressPurpose.CONTEXT_MENU

    def clear_press_purpose(self):
        self.__press_purpose = PressPurpose.NONE

    def wheelEvent(self, a0: typing.Optional[QtGui.QWheelEvent]):
        if a0.angleDelta().y() > 0:
            self.decrease_index()
        else:
            self.increase_index()

    def keyPressEvent(self, event: QKeyEvent, /) -> None:
        content_width = self.__content_label.width()
        content_pos_x = self.__content_label.x()
        # invisible_width = content_width - self.size().width() + ReaderConstants.CONTENT_SCROLL_RIGHT_MARGIN
        invisible_width = content_width - self.size().width()
        if event.key() == Qt.Key.Key_Left:
            if content_pos_x < 0:
                self.__content_label.move(min(self.__content_label.x() + 10, 0), self.__content_label.y())
            else:
                pass
                # 暂时放弃掉这个功能
                # self.decrease_index()
        elif event.key() == Qt.Key.Key_Right:
            if invisible_width > 0 and content_pos_x > -invisible_width:
                self.__content_label.move(content_pos_x - 3, self.__content_label.y())
            else:
                pass
                # 暂时放弃掉这个功能
                # self.increase_index()
        elif event.key() == Qt.Key.Key_Up:
            self.decrease_index()
        elif event.key() == Qt.Key.Key_Down:
            self.increase_index()

    def increase_index(self):
        if self.__current_reader is None:
            return
        lines = len(self.__current_reader.get_parsed_data())
        self.__index = self.__index + 1 if self.__index < lines - 1 else lines - 1
        self.emit_contents_changed()

    def decrease_index(self):
        if self.__current_reader is None:
            return
        self.__index = self.__index - 1 if self.__index > 0 else 0
        self.emit_contents_changed()

    def show_context_menu(self, pos):
        menu = QMenu()
        self.show_file_select_menu(menu)
        self.show_force_to_top_menu(menu)
        self.show_jump_to_chapter_menu(menu)
        menu.addSeparator()
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

    def show_jump_to_chapter_menu(self, menu):
        if self.__current_reader is None:
            return
        action = menu.addAction('跳转到章节')
        action.triggered.connect(lambda: self.show_chapter_dialog())

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
        self.__content_label.move(0, 0)
        self.__content_label.setText(resource.get_data())
        style_sheet = f"color: {config.get_font_color().name()}; "
        font = config.get_font()
        font.setPointSize(config.get_font_size())
        if resource.get_type() != ResourceType.TEXT:
            font.setBold(True)
            style_sheet += "text-decoration: underline; "
        self.__content_label.setFont(font)
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

    def show_chapter_dialog(self):
        if self.__current_reader is not None:
            self.__chapter_dialog.show_chapter_map(self.__current_reader.get_chapter_map())

    def recover_window(self):
        self.show()
        self.activateWindow()

    def quit_app(self):
        self.__tray_icon.hide()
        QApplication.exit()
        config.save_config()

    def refresh_window_style(self):
        self.setStyleSheet(f"background-color: {config.get_bg_color().name()}")
        self.resize(self.size().width(), config.get_font_size() * 4 / 3 + 4)
        # self.show()

    def init_window_style(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.resize(config.get_window_width(), config.get_font_size() * 4 / 3 + 4)
        # self.setFixedHeight(20)
        self.setMinimumWidth(200)
        self.setMaximumWidth(800)
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

    def init_chapter_dialog(self):
        self.__chapter_dialog.set_jump_to_chapter_callback(self.jump_to_chapter)

    def jump_to_chapter(self, index):
        self.__index = index
        self.emit_contents_changed()

    def emit_window_style_changed(self):
        self.__window_style_changed.emit()

    def emit_contents_changed(self):
        self.__contents_changed.emit()
