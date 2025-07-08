from file_readers.file_reader import FileReader
from file_readers.Resource import ResourceType, Resource
from ebooklib import epub


class EPUBFileReader(FileReader):
    def read_file(self, file_path):
        for data in super().get_test_data():
            self._parsed_data.append(Resource(ResourceType.TEXT, data))

        book = epub.read_epub(file_path)
        for item in book.get_items():
            print('type: \n')
            print(item.get_type())
            print('name: \n')
            print(item.get_name())
            print(item.get_content())
