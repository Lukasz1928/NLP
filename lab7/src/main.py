import json
import random
from sklearn.manifold import TSNE
from gensim.models import KeyedVectors
import matplotlib.pyplot as plt


def read_model():
    return KeyedVectors.load_word2vec_format('data/model.txt', binary=False)


def get_similar(model, words):
    return [x[0] for x in model.most_similar(positive=words, topn=5)]


def get_phrase(w):
    return " ".join([x.split(':')[0] for x in w])


def find_most_similar(model):
    phrases = [
        ['sąd::noun', 'wysoki::adj'],
        ['trybunał::noun', 'konstytucyjny::adj'],
        ['kodeks::noun', 'cywilny::adj'],
        ['kpk::noun'],
        ['sąd::noun', 'rejonowy::adj'],
        ['szkoda::noun'],
        ['wypadek::noun'],
        ['kolizja::noun'],
        ['szkoda::noun', 'majątkowy::adj'],
        ['nieszczęście::noun'],
        ['rozwód::noun']
    ]
    most_similar = {tuple(p): get_similar(model, p) for p in phrases}
    with open('results/most_similar.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps({get_phrase(k): v for k, v in most_similar.items()}, indent=2, ensure_ascii=False))


def calculate_equation(model, pos, neg):
    return [x[0] for x in model.most_similar(positive=pos, negative=neg, topn=5)]


def find_equations_results(model):
    with open('results/equations.txt', 'w+', encoding='utf-8') as f:
        f.write('sąd wysoki - kpc + konstytucja:\n')
        for x in calculate_equation(model, ['sąd::noun', 'wysoki::adj', 'konstytucja::noun'], ['kpc::noun']):
            f.write('{}\n'.format(x))
        f.write('\npasażer - mężczyzna + kobieta:\n')
        for x in calculate_equation(model, ['pasażer::noun', 'kobieta::noun'], ['mężczyzna::noun']):
            f.write('{}\n'.format(x))
        f.write('\nsamochód - droga + rzeka:\n')
        for x in calculate_equation(model, ['samochód::noun', 'rzeka::noun'], ['droga::noun']):
            f.write('{}\n'.format(x))


def find_vector(model, word):
    try:
        v = model[word]
    except KeyError:
        return None
    return v


def find_projection(model):
    words = ['szkoda::noun', 'strata::noun', 'szkoda_majątkowa::noun',
             'uszczerbek_na_zdrowie::noun', 'krzywda::noun',
             'niesprawiedliwość::noun', 'nieszczęście::noun']
    random_vectors = random.sample([model[k] for k in model.vocab.keys()], k=1000)
    words_vectors = [x for x in [find_vector(model, x) for x in words] if x is not None]

    projection = TSNE(n_components=2).fit_transform(random_vectors + words_vectors)
    plt.scatter(x=[x[0] for x in projection][len(words_vectors):], y=[x[1] for x in projection][len(words_vectors):], c='green', label='random words')
    plt.scatter(x=[x[0] for x in projection][0:len(words_vectors)], y=[x[1] for x in projection][0:len(words_vectors)], c='red', label='given words')
    plt.savefig('results/projection.png')


def main():
    model = read_model()
    find_most_similar(model)
    find_equations_results(model)
    find_projection(model)


if __name__ == "__main__":
    main()
