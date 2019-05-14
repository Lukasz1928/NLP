import numpy as np

from sklearn import svm, metrics
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline


def save(results_full, results_tenth, results_ten, results_single, results):
    results.results['svm']['full_text'].update(results_full)
    results.results['svm']['tenth_of_text'].update(results_tenth)
    results.results['svm']['ten_lines_of_text'].update(results_ten)
    results.results['svm']['single_line_of_text'].update(results_single)


def svm_classify(data_full, data_tenth, data_ten, data_single, labels, results, test, train, validation):
    results_full = classify(data_full, labels, test, train, validation)
    results_tenth = classify(data_tenth, labels, test, train, validation)
    results_ten = classify(data_ten, labels, test, train, validation)
    results_single = classify(data_single, labels, test, train, validation)
    save(results_full, results_tenth, results_ten, results_single, results)


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

    cls = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=10, tol=None))])
    cls.fit(train_data, train_labels)
    predicted = cls.predict(validation_data)
    precision, recall, f1, _ = precision_recall_fscore_support(validation_labels, predicted, average='binary')
    return {
        'accuracy': float("{:.3f}".format(round(precision, 3))),
        'recall': float("{:.3f}".format(round(recall, 3))),
        'f1': float("{:.3f}".format(round(f1, 3)))
    }
