from os import path
from pathlib import Path


class FileUtility:
    BASE_PATH = Path(__file__).parent.parent

    @staticmethod
    def get_file_path(*, file_name: str, relative_directory: str = 'resources'):
        """Get full file_path using file_name and relative directory"""
        return path.join(FileUtility.BASE_PATH, relative_directory, file_name).replace('\\', '/')

    @staticmethod
    def get_directory(*, relative_directory: str = 'reports'):
        """Get full directory path using relative directory"""
        return path.join(FileUtility.BASE_PATH, relative_directory).replace('\\', '/')
