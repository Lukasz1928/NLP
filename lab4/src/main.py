import numpy as np
from src.file_utils import get_data, save_results
import regex
import nltk


def prepare_text(text):
    text = regex.sub(r'[()?!.,:;\"\'\[\]\}\{\-_+=*&^%$#@|]', ' ', text) # ???
    text = regex.sub(r'\s+', ' ', text)
    text = text.lower()
    return text


def calculate_unigrams_and_bigrams(data):
    bigrams = {}
    unigrams = {}
    for d in data:
        text = prepare_text(d)
        tokens = nltk.word_tokenize(text, 'polish')
        for t in tokens:
            if t in unigrams.keys():
                unigrams[t] += 1
            else:
                unigrams[t] = 1
        bg = list(nltk.bigrams(tokens))
        for b in bg:
            if b[0].isalpha() and b[1].isalpha():
                if b in bigrams.keys():
                    bigrams[b] += 1
                else:
                    bigrams[b] = 1
    return unigrams, bigrams


def calculate_PMI(unigrams, bigrams):
    total_unigrams = sum(unigrams.values())
    total_bigrams = sum(bigrams.values())
    pmis = {}
    for (b1, b2) in bigrams.keys():
        prob1 = unigrams[b1] / total_unigrams
        prob2 = unigrams[b2] / total_unigrams
        prob12 = bigrams[(b1, b2)] / total_bigrams
        pmis[(b1, b2)] = np.log2(prob12 / (prob1 * prob2))
    return pmis


def main():
    data = get_data()
    unigrams, bigrams = calculate_unigrams_and_bigrams(data.values())
    pmis = calculate_PMI(unigrams, bigrams)
    sorted_pmis = sorted([(k, v) for (k, v) in pmis.items()], key=lambda x: x[1], reverse=True)[:30]

    
    save_results(bigrams, sorted_pmis)


if __name__ == "__main__":
    main()