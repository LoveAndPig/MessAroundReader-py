from file_readers.Resource import ResourceType, Resource
from history.history import history


class ReaderScroller:
    def __init__(self, reader):
        self.__reader = reader
        self.__index = 0
        self.__inner_index = 0

    def scroll_to_next(self):
        if self.__reader is None:
            return
        lines = len(self.__reader.get_parsed_data())
        self.__index = self.__index + 1 if self.__index < lines - 1 else lines - 1
        # self.update_history()

    def scroll_to_previous(self):
        if self.__reader is None:
            return
        self.__index = self.__index - 1 if self.__index > 0 else 0
        # self.update_history()

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
