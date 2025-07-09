from file_readers.Resource import Resource, ResourceType
from file_readers.file_reader import FileReader
import docx2txt


class WordFileReader(FileReader):
    def read_file(self, file_path):
        text = docx2txt.process(file_path)
        for line in text.split("\n"):
            strip_line = line.strip()
            if strip_line != "":
                self._parsed_data.append(Resource(ResourceType.TEXT, strip_line))

        self.make_chapter_list()
