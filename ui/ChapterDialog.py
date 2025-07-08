from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDialog, QListView, QVBoxLayout


class ChapterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__chapters_view = QListView()
        self.__model = QStandardItemModel()  # 初始化模型
        self.__chapters_view.setModel(self.__model)
        self.__jump_to_chapter_callback = None
        self.__current_chapter_map = {}

        layout = QVBoxLayout()
        layout.addWidget(self.__chapters_view)
        self.setLayout(layout)

        self.__chapters_view.doubleClicked.connect(self.jump_to_chapter)

    def show_chapter_map(self, chapter_map: dict):
        self.__current_chapter_map = chapter_map
        self.__model.clear()  # 清空上一次的数据

        for key in chapter_map:
            item = QStandardItem(key)
            item.setEditable(False)  # 禁止编辑
            self.__model.appendRow(item)

        self.show()

    def set_jump_to_chapter_callback(self, callback):
        self.__jump_to_chapter_callback = callback

    def jump_to_chapter(self, index):
        if self.__jump_to_chapter_callback and index.isValid():
            item = self.__model.itemFromIndex(index)
            chapter_name = item.text()
            line_index = self.__current_chapter_map[chapter_name]
            if line_index is not None:
                self.__jump_to_chapter_callback(line_index)

