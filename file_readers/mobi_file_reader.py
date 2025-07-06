from file_readers.file_reader import FileReader


class MobiFileReader(FileReader):
    def read_file(self, file_path):
        super().__parsed_data = super().get_test_data()
