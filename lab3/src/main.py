from elasticsearch import Elasticsearch
from src.es_utils import create_index, load_data
from src.file_utils import get_all_filenames, read_polimorfologik, save_results
import matplotlib.pyplot as plt
import Levenshtein


def aggregate_terms(terms):
    words = {}
    for doc in terms:
        term_vectors = doc['term_vectors']['text']
        for k, v in term_vectors['terms'].items():
            if k in words.keys():
                words[k] += v['term_freq']
            else:
                words[k] = v['term_freq']
    freqs = []
    freqs_dict = {}
    for w in words.keys():
        if len(w) > 1 and w.isalpha():
            freqs.append((w, words[w]))
            freqs_dict[w] = words[w]
    return sorted(freqs, key=lambda x: x[1], reverse=True), freqs_dict


def get_term_vectors(es, index_name):
    files = get_all_filenames()
    data = []
    for f in files:
        ret = es.termvectors(index_name, doc_type='doc', fields=['text'], id=f)
        data.append(ret)
    return data


def plot_frequencies(freqs):
    xs = [x + 1 for x in range(len(freqs))]
    ys = [freqs[i][1] for i in range(len(xs))]
    plt.plot(xs, ys, '.')
    plt.xlabel('word rank')
    plt.ylabel('word appearances')
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('results/frequencies.png')


def find_words_not_in_dictionary(words, dictionary):
    not_in_dict = []
    for w in words:
        if w[0] not in dictionary:
            not_in_dict.append(w)
    return not_in_dict


def find_top_words_not_in_dictionary(words):
    return sorted(words, key=lambda w: w[1], reverse=True)[:30]


def find_top_words_not_in_dictionary_with_3_occurences(words):
    return [w for w in words if w[1] == 3][:30]


def find_most_probable_corrections(words, frequencies, dictionary):
    corrections = []
    for w in words:
        min_dist = 99999
        possible_corrections = []
        for d in dictionary:
            dist = Levenshtein.distance(w[0], d)
            if dist < min_dist:
                min_dist = dist
                possible_corrections = [d]
            elif dist == min_dist:
                possible_corrections.append(d)
        best_correction = max(possible_corrections, key=lambda w: frequencies[w] if w in frequencies.keys() else -1)
        corrections.append((w[0], best_correction))
    return corrections


def main():
    index_name = 'idx'
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    pm = read_polimorfologik()

    create_index(es, index_name)
    load_data(es, index_name)
    tv = get_term_vectors(es, index_name)
    agg, agg_dict = aggregate_terms(tv)
    plot_frequencies(agg)
    words_not_in_dict = find_words_not_in_dictionary(agg, pm)
    top_words_not_in_dict = find_top_words_not_in_dictionary(words_not_in_dict)
    words_not_in_dict_with_3_occurrences = find_top_words_not_in_dictionary_with_3_occurences(words_not_in_dict)
    corrections = find_most_probable_corrections(words_not_in_dict_with_3_occurrences, agg_dict, pm)

    save_results(words_not_in_dict, top_words_not_in_dict, words_not_in_dict_with_3_occurrences, corrections)


if __name__ == "__main__":
    main()
