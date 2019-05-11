from src.data_utils import split_data, remove_titles, split_test_train_validation, get_random_lines
from src.fast_text import fasttext_classify
from src.file_utils import get_data
from src.results import Results
from src.svm import svm_classify


def main():
    data = get_data()
    amending, not_amending = split_data(data)
    data = remove_titles(data)
    test, train, validation = split_test_train_validation(set(data.keys()))

    labels = {k: 1 if k in amending else 0 for k in data.keys()}
    full_text_documents = data
    tenth_of_text_documents = {k: get_random_lines(v, 10, percentage=True) for k, v in data.items()}
    ten_lines_documents = {k: get_random_lines(v, 10) for k, v in data.items()}
    single_line_documents = {k: get_random_lines(v, 1) for k, v in data.items()}

    r = Results()

    #svm_classify(full_text_documents, tenth_of_text_documents, ten_lines_documents, single_line_documents, labels, r, test, train, validation)
    fasttext_classify(full_text_documents, tenth_of_text_documents, ten_lines_documents, single_line_documents, labels, r, test, train, validation)

    r.save('results.json')


if __name__ == "__main__":
    main()
