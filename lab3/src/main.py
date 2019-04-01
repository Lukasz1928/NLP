from elasticsearch import Elasticsearch
from src.es_utils import create_index, load_data
from src.file_utils import get_all_filenames, read_polimorfologik, save_results
import matplotlib.pyplot as plt


def aggregate_terms(terms):
    words = {}
    total_words = 0
    for doc in terms:
        term_vectors = doc['term_vectors']['text']
        for k, v in term_vectors['terms'].items():
            if k in words.keys():
                words[k] += v['term_freq']
            else:
                words[k] = v['term_freq']
            total_words += v['term_freq']
    freqs = []
    for w in words.keys():
        if len(w) > 1 and w.isalpha():
            freqs.append((w, words[w]))
    return sorted(freqs, key=lambda x: x[1], reverse=True)


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
    plt.show()


def levenshtein_distance(s1, s2):
    m = len(s1) + 1
    n = len(s2) + 1
    d = [[0] * n for _ in range(m)]
    for i in range(m):
        d[i][0] = i
    for i in range(n):
        d[0][i] = i
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            d[i][j] = min([d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost])
    return d[m - 1][n - 1]


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


def find_most_probable_corrections(words, frequencies):
    return []


def main():
    index_name = 'idx'
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    pm = read_polimorfologik()

    create_index(es, index_name)
    load_data(es, index_name)
    tv = get_term_vectors(es, index_name)
    agg = aggregate_terms(tv)
    plot_frequencies(agg)
    words_not_in_dict = find_words_not_in_dictionary(agg, pm)
    top_words_not_in_dict = find_top_words_not_in_dictionary(words_not_in_dict)
    words_not_in_dict_with_3_occurences = find_top_words_not_in_dictionary_with_3_occurences(words_not_in_dict)
    corrections = find_most_probable_corrections(top_words_not_in_dict, agg)

    save_results(words_not_in_dict, top_words_not_in_dict, words_not_in_dict_with_3_occurences, corrections)


if __name__ == "__main__":
    main()
