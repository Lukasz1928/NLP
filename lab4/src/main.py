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
        tokens = text.split(" ")
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


vf = np.vectorize(lambda x, N: (x / N) * np.log((x / N) + (1 if x == 0 else 0)))


def H(k):
    return np.sum(vf(k, np.sum(k)))


def LLR(k):
    return 2 * np.sum(k) * (H(k) - (H(np.sum(k, axis=0)) + H(np.sum(k, axis=1))))


def calculate_LLR(unigrams, bigrams):
    llrs = {}
    s = sum(bigrams.values())
    for bigram in bigrams.keys():
        k = np.zeros([2, 2])
        k[0][0] = bigrams[bigram]  # both words together
        k[0][1] = unigrams[bigram[1]] - bigrams[bigram]  # only first word
        k[1][0] = unigrams[bigram[0]] - bigrams[bigram]  # only second word
        k[1][1] = s - (k[0][0] + k[0][1] + k[1][0])  # neither word
        llrs[bigram] = LLR(k)
    return llrs


def main():
    data = get_data()
    unigrams, bigrams = calculate_unigrams_and_bigrams(data.values())
    pmis = calculate_PMI(unigrams, bigrams)
    sorted_pmis = sorted([(k, v) for (k, v) in pmis.items()], key=lambda x: x[1], reverse=True)[:30]

    llrs = calculate_LLR(unigrams, bigrams)
    sorted_llrs = sorted([(k, v) for (k, v) in llrs.items()], key=lambda x: x[1], reverse=True)[:30]

    save_results(bigrams, sorted_pmis, sorted_llrs)


if __name__ == "__main__":
    main()