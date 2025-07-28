from abc import abstractmethod, ABC
from file_readers.Resource import Resource, ResourceType
from utils.regex import regex_util
from file_readers.reader_scroller import ReaderScroller

test_data = [
    # 基础测试
    "a",
    "A",
    "",
    " ",

    # 特殊字符
    "Hello, World!",
    "C++_is_Awesome!",
    "测试数据🤣",
    "\\n\\t\\\\",
    "😎🚀✨",

    # 边界测试
    "The_Quick_Brown_Fox_Jumps_Over_The_Lazy_Dog",

    # 格式测试
    "JSON: {\"key\": \"value\"}",
    "XML: <root><test>data</test></root>",
    "CSV: Alice,25,New\\York",

    # 有趣测试
    "答案永远是42",
    "I solemnly swear I am up to no good",
    "01010100 01100101 01110011 01110100", # "Test"的二进制
    "To be or not to be, that is the question",

    # 极端情况
    "NULL",
    "nullptr",
    "undefined",
    "NaN",
    "Infinity",

    # 程序员幽默
    "// TODO: Remove this before production",
    "This is a FIXME comment",
    "It works on my machine",
    "Copy Paste Engineering",
    "99 little bugs in the code..."
]


class FileReader:
    def __init__(self):
        self._parsed_data = []
        self._chapter_map = {}

        self.__file_path = ""
        self.__scroller = ReaderScroller(self)
        self.__is_initialized = False

    def parse_file(self, file_path):
        if not self.__is_initialized:
            self.__file_path = file_path
            self.read_file(file_path)
            self.__is_initialized = True

    @abstractmethod
    def read_file(self, file_path):
        pass

    def get_parsed_data(self) -> list[Resource]:
        return self._parsed_data

    def get_chapter_map(self) -> dict:
        return self._chapter_map

    def add_chapter_index(self, chapter_name, index):
        self._chapter_map[chapter_name] = index

    def make_chapter_list(self):
        self._chapter_map.clear()
        for i, resource in enumerate(self._parsed_data):
            if resource.get_type() == ResourceType.TEXT:
                if regex_util.is_string_match_regex(resource.get_data()):
                    self.add_chapter_index(resource.get_data(), i)

    def scroll_to_next(self) -> bool:
        return self.__scroller.scroll_to_next()

    def scroll_to_previous(self) -> bool:
        return self.__scroller.scroll_to_previous()

    def is_scroll_after_new_available(self) -> bool:
        return self.__scroller.is_scroll_after_new_available()

    def get_index(self) -> int:
        return self.__scroller.get_index()

    def jump_to_index(self, index):
        self.__scroller.jump_to_index(index)

    def get_resource(self) -> Resource:
        return self.__scroller.get_resource()

    def get_text(self) -> str:
        return self.__scroller.get_text()

    def get_type(self) -> ResourceType:
        return self.__scroller.get_type()

    def get_file_path(self):
        return self.__file_path

    def update_history(self):
        self.__scroller.update_history()

    def update_reach_side(self, reach):
        self.__scroller.update_reach_side(reach)

    def set_scroll_no_gap(self, scroll_no_gap):
        self.__scroller.set_scroll_no_gap(scroll_no_gap)

    @staticmethod
    def get_test_data():
        test_resources = []
        for item in test_data:
            test_resources.append(Resource(ResourceType.TEXT, item))

        return test_resources
