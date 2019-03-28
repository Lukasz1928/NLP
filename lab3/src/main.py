from elasticsearch import Elasticsearch
from src.es_utils import create_index, load_data
from src.file_utils import get_all_filenames
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
    return freqs


def plot_frequencies(freqs):
    xs = [x + 1 for x in range(len(freqs))]
    sorted_frequencies = sorted(freqs, key=lambda x: x[1], reverse=True)
    ys = [sorted_frequencies[i][1] for i in range(len(xs))]
    plt.plot(xs, ys, '.')
    plt.xlabel('word rank')
    plt.ylabel('word appearances')
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('results/frequencies.png')
    plt.show()


def main():
    index_name = 'idx'
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    create_index(es, index_name)
    load_data(es, index_name)
    files = get_all_filenames()
    data = []
    for f in files:
        ret = es.termvectors(index_name, doc_type='doc', fields=['text'], id=f)
        data.append(ret)
    agg = aggregate_terms(data)
    plot_frequencies(agg)


if __name__ == "__main__":
    main()
