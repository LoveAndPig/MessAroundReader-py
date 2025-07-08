from file_readers.file_reader import FileReader
from file_readers.Resource import ResourceType, Resource
from utils.regex import regex_util


class TextFileReader(FileReader):
    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    if line.strip() != '':
                        self._parsed_data.append(Resource(ResourceType.TEXT, line))

            self.make_chapter_list()
            print(len(self.get_parsed_data()))
        except Exception as e:
            print(e)
