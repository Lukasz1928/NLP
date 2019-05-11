import fasttext
import regex


def save(results_full, results_tenth, results_ten, results_single, results):
    results.results['fasttext']['full_text'].update(results_full)
    results.results['fasttext']['tenth_of_text'].update(results_tenth)
    results.results['fasttext']['ten_lines_of_text'].update(results_ten)
    results.results['fasttext']['single_line_of_text'].update(results_single)


def fasttext_classify(data_full, data_tenth, data_ten, data_single, labels, results, test, train, validation):
    results_full = classify(data_full, labels, test, train, validation)
    results_tenth = classify(data_tenth, labels, test, train, validation)
    results_ten = classify(data_ten, labels, test, train, validation)
    results_single = classify(data_single, labels, test, train, validation)
    save(results_full, results_tenth, results_ten, results_single, results)


def save_training_file(data, labels):
    with open('training.txt', 'w+', encoding='utf-8') as f:
        for k in range(len(data)):
            f.write('__label__{} {}\n'.format(labels[k], data[k]))


def classify(data, labels, test, train, validation):
    train_data = [k for k in data.keys() if k in train]
    train_labels = [labels[k] for k in train_data]
    train_data = [data[k] for k in train_data]

    test_data = [k for k in data.keys() if k in test]
    test_labels = [labels[k] for k in test_data]
    test_data = [data[k] for k in test_data]

    validation_data = [k for k in data.keys() if k in validation]
    validation_labels = [labels[k] for k in validation_data]
    validation_data = [data[k] for k in validation_data]

    save_training_file(train_data, train_labels)

    cls = fasttext.supervised('training.txt', 'model')
    predicted = cls.predict(test_data)
