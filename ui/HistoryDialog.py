from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDialog, QListView, QVBoxLayout

from history.history import history
import os


class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("历史记录")
        self.__history_view = QListView()
        self.__model = QStandardItemModel()  # 初始化模型
        self.__history_view.setModel(self.__model)
        self.__recover_from_history_callback = None

        layout = QVBoxLayout()
        layout.addWidget(self.__history_view)
        self.setLayout(layout)

        self.__history_view.doubleClicked.connect(self.recover_from_history)

    def show_history(self):
        self.__model.clear()

        for file_path, index in history.get_history().items():
            file_name = os.path.basename(file_path)
            item = QStandardItem(f"{index} --- {file_name}")
            item.setEditable(False)
            item.setData((file_path, index))
            self.__model.appendRow(item)

        self.show()

    def set_recover_from_history_callback(self, callback):
        self.__recover_from_history_callback = callback

    def recover_from_history(self, view_index):
        if self.__recover_from_history_callback is not None:
            file_path, index = self.__model.itemFromIndex(view_index).data()
            self.__recover_from_history_callback(file_path)
