from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QCloseEvent
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from constants import ShorCutTarget
from config.configuration import config
from utils.key_utils import KeyUtils


class ShortCutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("快捷键")

        # self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.__short_cut_target = ShorCutTarget.NONE
        self.__btn_ready = None

        self.init_ui()

    def init_ui(self):
        keys_layout = QVBoxLayout(self)

        keys_layout.addLayout(self.create_key_box(ShorCutTarget.PREVIOUS_LINE))
        keys_layout.addLayout(self.create_key_box(ShorCutTarget.NEXT_LINE))
        keys_layout.addLayout(self.create_key_box(ShorCutTarget.MOVE_BACKWARD))
        keys_layout.addLayout(self.create_key_box(ShorCutTarget.MOVE_FORWARD))

    def create_key_box(self, target: ShorCutTarget):
        key_box = QHBoxLayout(self)

        def get_key_label():
            if target == ShorCutTarget.PREVIOUS_LINE:
                return "上一行"
            elif target == ShorCutTarget.NEXT_LINE:
                return "下一行"
            elif target == ShorCutTarget.MOVE_FORWARD:
                return "前进"
            elif target == ShorCutTarget.MOVE_BACKWARD:
                return "后退"

        key_label = QLabel(get_key_label())
        key_label.show()
        key_box.addWidget(key_label)

        def get_key_description():
            if target == ShorCutTarget.PREVIOUS_LINE:
                return KeyUtils.get_key_description(config.get_previous_line_key())
            elif target == ShorCutTarget.NEXT_LINE:
                return KeyUtils.get_key_description(config.get_next_line_key())
            elif target == ShorCutTarget.MOVE_FORWARD:
                return KeyUtils.get_key_description(config.get_move_forward_key())
            elif target == ShorCutTarget.MOVE_BACKWARD:
                return KeyUtils.get_key_description(config.get_move_backward_key())

        key_btn = QPushButton(self)
        key_btn.setText(get_key_description())
        key_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        key_btn.setFixedWidth(100)
        key_btn.clicked.connect(lambda: self.key_btn_clicked(key_btn, target))
        key_box.addWidget(key_btn)

        return key_box

    def key_btn_clicked(self, btn, target):
        self.__short_cut_target = target
        self.__btn_ready = btn

        btn.setText("按下新的按键")
        btn.show()

    def keyPressEvent(self, event: QKeyEvent, /) -> None:
        if self.__btn_ready is not None and self.__short_cut_target != ShorCutTarget.NONE:
            key = event.key()

            self.update_keys(key)
            # self.exec()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent, /) -> None:
        if self.__btn_ready is not None and self.__short_cut_target != ShorCutTarget.NONE:
            key = Qt.Key.Key_unknown
            if self.__short_cut_target == ShorCutTarget.PREVIOUS_LINE:
                key = config.get_previous_line_key()
            elif self.__short_cut_target == ShorCutTarget.NEXT_LINE:
                key = config.get_next_line_key()
            elif self.__short_cut_target == ShorCutTarget.MOVE_FORWARD:
                key = config.get_move_forward_key()
            elif self.__short_cut_target == ShorCutTarget.MOVE_BACKWARD:
                key = config.get_move_backward_key()

            self.update_keys(key)

        self.finish()

    def update_keys(self, key):
        if self.__short_cut_target == ShorCutTarget.PREVIOUS_LINE:
            config.set_previous_line_key(key)
        elif self.__short_cut_target == ShorCutTarget.NEXT_LINE:
            config.set_next_line_key(key)
        elif self.__short_cut_target == ShorCutTarget.MOVE_FORWARD:
            config.set_move_forward_key(key)
        elif self.__short_cut_target == ShorCutTarget.MOVE_BACKWARD:
            config.set_move_backward_key(key)

        key_desc = KeyUtils.get_key_description(key)
        if self.__btn_ready is not None:
            self.__btn_ready.setText(key_desc)
            self.__btn_ready.show()

        self.finish()

    def set_short_cut_target(self, short_cut_target: ShorCutTarget):
        self.__short_cut_target = short_cut_target

    def finish(self):
        self.set_short_cut_target(ShorCutTarget.NONE)
        self.__btn_ready = None
