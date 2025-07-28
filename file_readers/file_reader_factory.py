from file_readers.epub_file_reader import EPUBFileReader
from file_readers.mobi_file_reader import MobiFileReader
from file_readers.word_file_reader import WordFileReader
from file_readers.text_file_reader import TextFileReader
from utils.file_utils import FileUtils


class FileReaderFactory:
    __reader_dict = {}

    def create_file_reader(self, file_path):
        if self.is_text_file(file_path):
            return TextFileReader()
        elif self.is_epub_file(file_path):
            return EPUBFileReader()
        elif self.is_word_file(file_path):
            return WordFileReader()
        elif self.is_mobi_file(file_path):
            return MobiFileReader()
        else:
            return None

    def get_file_reader(self, file_path):
        if not FileUtils.is_file_exists(file_path):
            return None

        if file_path in self.__reader_dict:
            return self.__reader_dict[file_path]
        else:
            reader = self.create_file_reader(file_path)
            self.__reader_dict[file_path] = reader
            return reader

    def is_text_file(self, file_path: str):
        return file_path.endswith('.txt')

    def is_epub_file(self, file_path: str):
        return file_path.endswith('.epub')

    def is_mobi_file(self, file_path: str):
        return file_path.endswith('.mobi') or file_path.endswith('.azw3')

    def is_word_file(self, file_path: str):
        return file_path.endswith('.docx') or file_path.endswith('.doc')


file_reader_factory = FileReaderFactory()
