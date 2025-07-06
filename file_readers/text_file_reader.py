from file_readers.file_reader import FileReader
from file_readers.Resource import ResourceType, Resource


class TextFileReader(FileReader):
    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    self._parsed_data.append(Resource(ResourceType.TEXT, line))

            print(len(self.get_parsed_data()))
        except Exception as e:
            print(e)
