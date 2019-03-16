import regex

from src.external import find_external_references
from src.file_utils import get_data, pprint

if __name__ == "__main__":
    data = get_data()
    print(find_external_references(data))
