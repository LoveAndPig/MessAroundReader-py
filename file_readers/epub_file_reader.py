import ebooklib

from file_readers.file_reader import FileReader
from file_readers.Resource import ResourceType, Resource
from ebooklib import epub
import bs4


class EPUBFileReader(FileReader):
    def read_file(self, file_path):
        book = epub.read_epub(file_path)
        image_count = 0
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = bs4.BeautifulSoup(item.get_content(), 'html.parser')
                content = soup.get_text()
                lines = content.split('\n')
                for line in lines:
                    if line.strip() != '':
                        self._parsed_data.append(Resource(ResourceType.TEXT, line))
            elif item.get_type() == ebooklib.ITEM_IMAGE:
                self._parsed_data.append(Resource(ResourceType.IMAGE, item.get_content()))

        self.make_chapter_list()
