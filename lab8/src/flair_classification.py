import os
from flair.data import TaggedCorpus, Sentence
from flair.data_fetcher import NLPTaskDataFetcher, NLPTask
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentRNNEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
import regex
from pathlib import Path
from sklearn.metrics import precision_recall_fscore_support


def save(results_full, results_tenth, results_ten, results_single, results):
    results.results['flair']['full_text'].update(results_full)
    results.results['flair']['tenth_of_text'].update(results_tenth)
    results.results['flair']['ten_lines_of_text'].update(results_ten)
    results.results['flair']['single_line_of_text'].update(results_single)


def save_training_files(train_data, train_labels, test_data, test_labels, validation_data, validation_labels):
    with open('train.txt', 'w+', encoding='utf-8') as f:
        for k in range(len(train_data)):
            f.write('__label__{} {}\n'.format(train_labels[k], regex.sub(r'\n', ' ', train_data[k])))
    with open('test.txt', 'w+', encoding='utf-8') as f:
        for k in range(len(test_data)):
            f.write('__label__{} {}\n'.format(test_labels[k], regex.sub(r'\n', ' ', test_data[k])))
    with open('dev.txt', 'w+', encoding='utf-8') as f:
        for k in range(len(validation_data)):
            f.write('__label__{} {}\n'.format(validation_labels[k], regex.sub(r'\n', ' ', validation_data[k])))


def remove_training_files():
    try:
        os.remove('train.txt')
    except FileNotFoundError:
        pass
    try:
        os.remove('test.txt')
    except FileNotFoundError:
        pass
    try:
        os.remove('dev.txt')
    except FileNotFoundError:
        pass


def flair_classify(data_full, data_tenth, data_ten, data_single, labels, results, test, train, validation):
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

    save_training_files(train_data, train_labels, test_data, test_labels, validation_data, validation_labels)
    corpus = NLPTaskDataFetcher.load_classification_corpus(Path('./'), test_file='test.txt', dev_file='dev.txt', train_file='train.txt')
    word_embeddings = [FlairEmbeddings('multi-forward')]
    doc_embeddings = DocumentRNNEmbeddings(word_embeddings, hidden_size=512, reproject_words=True, reproject_words_dimension=256)
    classifier = TextClassifier(doc_embeddings, label_dictionary=corpus.make_label_dictionary(), multi_label=False)
    trainer = ModelTrainer(classifier, corpus)
    trainer.train('./', max_epochs=25)
    classifier = TextClassifier.load_from_file('./best-model.pt')

    validation_data = [Sentence(x) for x in validation_data]
    for x in validation_data:
        classifier.predict(x)
    predicted = [int(x.labels[0].value) for x in validation_data]
    remove_training_files()
    precision, recall, f1, _ = precision_recall_fscore_support(validation_labels, predicted, average='binary')
    return {
        'accuracy': float("{:.3f}".format(round(precision, 3))),
        'recall': float("{:.3f}".format(round(recall, 3))),
        'f1': float("{:.3f}".format(round(f1, 3)))
    }