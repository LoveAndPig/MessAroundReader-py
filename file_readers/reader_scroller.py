import time

from file_readers.Resource import ResourceType, Resource
from history.history import history
from config.configuration import config


class ReaderScroller:
    def __init__(self, reader):
        self.__reader = reader
        self.__index = 0
        self.__inner_index = 0

        self.__is_reach_side = False
        self.__reach_side_time = time.perf_counter()

        self.__switch_to_new_line_time = time.perf_counter()

    def scroll_to_next(self) -> bool:
        if self.__reader is None:
            return False
        self.update_reach_side(True)
        lines = len(self.__reader.get_parsed_data())
        # self.__index = self.__index + 1 if self.__index < lines - 1 else lines - 1
        if self.is_scroll_to_new_available() and self.__index < lines - 1:
            self.__index += 1
            self.__is_reach_side = False
            self.__switch_to_new_line_time = time.perf_counter()
            return True

        return False

    def scroll_to_previous(self) -> bool:
        if self.__reader is None:
            return False
        self.update_reach_side(True)
        # self.__index = self.__index - 1 if self.__index > 0 else 0
        if self.is_scroll_to_new_available() and self.__index > 0:
            self.__index -= 1
            self.__is_reach_side = False
            self.__switch_to_new_line_time = time.perf_counter()
            return True

        return False

    def update_reach_side(self, reach):
        if reach != self.__is_reach_side:
            self.__reach_side_time = time.perf_counter()
        self.__is_reach_side = reach

    def is_scroll_to_new_available(self) -> bool:
        if self.__reader is None:
            return False
        gap = time.perf_counter() - self.__reach_side_time
        return gap * 1000 > config.get_scroll_to_new_disable_gap()

    def is_scroll_after_new_available(self) -> bool:
        if self.__reader is None:
            return False
        gap = time.perf_counter() - self.__switch_to_new_line_time
        return gap * 1000 > config.get_scroll_after_new_disable_gap()

    def get_resource(self) -> Resource:
        if self.__reader is None:
            return Resource(ResourceType.TEXT, "选择一个文件")
        if 0 <= self.__index < len(self.__reader.get_parsed_data()):
            return self.__reader.get_parsed_data()[self.__index]

        return Resource(ResourceType.INVALID, "无效资源")

    def get_text(self) -> str:
        if self.__reader is None:
            return ""
        current_resource = self.get_resource()
        if current_resource.get_type() == ResourceType.TEXT:
            return current_resource.get_data()
        elif current_resource.get_type() == ResourceType.IMAGE:
            return "点击显示图片"
        elif current_resource.get_type() == ResourceType.LINK:
            return current_resource.get_data()
        else:
            return "无效资源"

    def get_type(self) -> ResourceType:
        return self.get_resource().get_type()

    def get_index(self) -> int:
        return self.__index

    def jump_to_index(self, index):
        self.__index = index
        self.__inner_index = 0
        # self.update_history()

    def update_history(self):
        history.update_history(self.__reader.get_file_path(), self.__index)
