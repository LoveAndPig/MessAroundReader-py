from file_readers.file_reader import FileReader
from file_readers.Resource import ResourceType, Resource
from utils.regex import regex_util


class TextFileReader(FileReader):
    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f.readlines()):
                    self._parsed_data.append(Resource(ResourceType.TEXT, line))
                    if regex_util.is_string_match_regex(line.strip()):
                        self.add_chapter_index(line.strip(), i)
                        print(line)

            print(len(self.get_parsed_data()))
        except Exception as e:
            print(e)
