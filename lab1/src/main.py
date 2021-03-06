from src.external import find_external_references
from src.file_utils import get_data
from src.occurences import count_ustawa_occurrences


if __name__ == "__main__":
    data = get_data()
    find_external_references(data, "external_references")
    count_ustawa_occurrences(data, "ustawa_word_count")
