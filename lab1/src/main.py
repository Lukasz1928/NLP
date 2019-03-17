import regex

from src.external import find_external_references
from src.file_utils import get_data
from src.internal import find_internal_references
from src.occurences import count_ustawa_occurrences


if __name__ == "__main__":
    # s = "aaa \n     bbb"
    # print(regex.sub(r'\s+', ' ', s))
    data = get_data()
    find_external_references(data, "external_references")
    # find_internal_references(data, "internal_references")
    # count_ustawa_occurrences(data, "ustawa_word_count")
