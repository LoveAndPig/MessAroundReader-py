import os


class FileUtils:
    @staticmethod
    def is_file_exists(file_path) -> bool:
        return os.path.exists(file_path)
