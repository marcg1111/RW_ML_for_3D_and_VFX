import json
import os
from dataclasses import dataclass, field

@dataclass
class Fstream:
    name: str
    path: str
    extension: str
    data_file: str = field(init=False)
    
    @classmethod
    def load_json_files(cls, path: str) -> dict:
        """
        Read json files from the given path.

        Args:
            path (str): The path to the directory containing the json files.

        Returns:
            dict: A hash map containing the json data.
        """
        with open(path, 'rb') as data_file:
            cls.data_file = json.load(data_file)

        return cls.data_file;

    @staticmethod
    def print_json_structure(data_file):
        for id, item in data_file["Items"].items():
            print(id, item);
