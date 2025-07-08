from abc import abstractmethod, ABC
from file_readers.Resource import Resource, ResourceType
from utils.regex import regex_util

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

    @staticmethod
    def get_test_data():
        test_resources = []
        for item in test_data:
            test_resources.append(Resource(ResourceType.TEXT, item))

        return test_resources
