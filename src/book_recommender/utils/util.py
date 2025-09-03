import yaml
import sys
from book_recommender.exception.exception_handler import WebAppException

def read_yaml_file(file_path: str) -> dict:
    """
    Read a YAML file and return its contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise WebAppException(e, sys) from e #type:ignore