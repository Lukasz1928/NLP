import regex

from src.external import find_external_references
from src.file_utils import get_data, pprint
from src.occurences import count_ustawa_occurrences

if __name__ == "__main__":
    data = get_data()
    count_ustawa_occurrences(data, "ustawa_word_count")
