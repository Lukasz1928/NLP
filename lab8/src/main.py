from src.data_utils import split_data, remove_titles, split_test_train_validation, get_random_lines
from src.file_utils import get_data


def main():
    data = get_data()
    amending, not_amending = split_data(data)
    data = remove_titles(data)
    test, train, validation = split_test_train_validation(amending + not_amending)

    labels = {k: True if k in amending else False for k in data.keys()}

    full_text_documents = data
    tenth_of_text_documents = {k: get_random_lines(v, 10, percentage=True) for k, v in data.items()}
    ten_lines_documents = {k: get_random_lines(v, 10) for k, v in data.items()}
    single_line_documents = {k: get_random_lines(v, 1) for k, v in data.items()}


if __name__ == "__main__":
    main()
