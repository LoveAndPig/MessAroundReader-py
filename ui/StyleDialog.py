from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QColorDialog, QFontComboBox

from config.configuration import config


class StyleDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.__window_style_changed_callback = None
        self.__contents_changed_callback = None

    def set_window_style_changed_callback(self, callback):
        self.__window_style_changed_callback = callback

    def set_contents_changed_callback(self, callback):
        self.__contents_changed_callback = callback

    def init_ui(self):
        self.setWindowTitle('设置样式')
        vbox = QVBoxLayout(self)

        bg_color_box = self.create_bg_color_box()
        vbox.addLayout(bg_color_box)

        font_color_box = self.create_font_color_box()
        vbox.addLayout(font_color_box)

        font_box = self.create_font_box()
        vbox.addLayout(font_box)

    def create_bg_color_box(self):
        bg_color_box = QHBoxLayout(self)

        bg_color_label = QLabel('背景颜色', self)
        bg_color_label.show()
        bg_color_box.addWidget(bg_color_label)

        bg_color_btn = QPushButton(self)
        bg_color_btn.setStyleSheet(f"background-color: {config.get_bg_color().name()}")

        def change_bg_color():
            color = QColorDialog.getColor()
            if color.isValid():
                bg_color_btn.setStyleSheet(f"background-color: {color.name()}")
                config.set_bg_color(color)
                config.save_config()
                if self.__window_style_changed_callback:
                    self.__window_style_changed_callback()
                self.exec()

        bg_color_btn.clicked.connect(lambda: change_bg_color())
        bg_color_btn.show()
        bg_color_box.addWidget(bg_color_btn)

        return bg_color_box

    def create_font_color_box(self):
        font_color_box = QHBoxLayout(self)

        font_color_label = QLabel('字体颜色', self)
        font_color_label.show()
        font_color_box.addWidget(font_color_label)

        font_color_btn = QPushButton(self)
        font_color_btn.setStyleSheet(f"background-color: {config.get_font_color().name()}")

        def change_font_color():
            color = QColorDialog.getColor()
            if color.isValid():
                font_color_btn.setStyleSheet(f"background-color: {color.name()}")
                config.set_font_color(color)
                config.save_config()
                if self.__contents_changed_callback:
                    self.__contents_changed_callback()
                self.exec()

        font_color_btn.clicked.connect(lambda: change_font_color())
        font_color_btn.show()
        font_color_box.addWidget(font_color_btn)

        return font_color_box

    def create_font_box(self):
        font_box = QHBoxLayout(self)

        font_label = QLabel('字  体', self)
        font_label.show()
        font_box.addWidget(font_label)

        font_combo_box = QFontComboBox(self)
        font_combo_box.setCurrentFont(config.get_font())

        def change_font(font):
            config.set_font(font.family())
            config.save_config()
            if self.__contents_changed_callback:
                self.__contents_changed_callback()

        font_combo_box.currentFontChanged.connect(lambda: change_font(font_combo_box.currentFont()))
        font_combo_box.show()
        font_box.addWidget(font_combo_box)

        return font_box
