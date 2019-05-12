import fasttext
import os

import regex
from sklearn.metrics import precision_recall_fscore_support


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
            f.write('__label__{} {}\n'.format(labels[k], regex.sub(r'\n', ' ', data[k])))


def remove_training_file():
    os.remove('training.txt')
    os.remove('model.bin')


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
    cls = fasttext.supervised('training.txt', 'model', lr_update_rate=200000, epoch=10, lr=0.3)
    predicted = [int(x[0]) for x in cls.predict(validation_data)]
    remove_training_file()
    precision, recall, f1, _ = precision_recall_fscore_support(validation_labels, predicted, average='binary')
    return {
        'accuracy': float("{:.3f}".format(round(precision, 3))),
        'recall': float("{:.3f}".format(round(recall, 3))),
        'f1': float("{:.3f}".format(round(f1, 3)))
    }
