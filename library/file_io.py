import json
import os
from dataclasses import dataclass, field

@dataclass
class Fstream:
    name: str
    path: str
    extension: str
    data_file: str = field(init=False)

    def __post_init__(self):
        self.data_file = os.path.join(self.path, f"{self.name}.{self.extension}")

    @staticmethod
    def load_json_file(file_path: str) -> dict:
        """
        Read a JSON file from the given file path.

        Args:
            file_path (str): The full path to the JSON file.

        Returns:
            dict: A dictionary containing the JSON data.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON file: {e}")
            return {}
        
    @staticmethod
    def print_json_structure(data):
        """
        Prints the structure of the JSON data assuming it contains an 'Items' dict.

        Args:
            data (dict): The JSON data loaded from a file.
        """
        if "Items" not in data:
            print("No 'Items' key found in the JSON data.")
            return

        for id, item in data["Items"].items():
            print(id, item)