import numpy as np
import regex

from src.file_utils import get_all_filenames, save_results
from requests import post


def tag_data(data):
    resp = post("http://localhost:9200", data=data.encode('utf-8'))
    return resp.text


def calculate_bigrams(words):
    bigrams = {}
    for i in range(len(words) - 1):
        bigram = (words[i], words[i + 1])
        if bigram in bigrams.keys():
            bigrams[bigram] += 1
        else:
            bigrams[bigram] = 1
    return bigrams


def calculate_unigrams(words):
    unigrams = {}
    for i in range(len(words)):
        unigram = words[i]
        if unigram in unigrams.keys():
            unigrams[unigram] += 1
        else:
            unigrams[unigram] = 1
    return unigrams


def sum_bigrams(bigrams):
    total = {}
    for v in bigrams.values():
        for k, bg in v.items():
            if k in total:
                total[k] += bg
            else:
                total[k] = bg
    return total


def filter_bigrams(bigrams):
    return {k: v for k, v in bigrams.items() if k[0].split(":")[0].isalpha() and k[1].split(":")[0].isalpha()}


def get_words(tagged):
    lines = [regex.sub(r"\s+", ":", regex.sub(r"^\s*", "", line)).lower() for line in tagged.split('\n')
             if line.endswith("disamb")]
    words = []
    for line in lines:
        tokens = regex.sub(r"\s+", ":", line).split(":")[:2]
        words.append('{}:{}'.format(*tokens))
    return words


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
    total_bigrams = {}
    total_unigrams = {}
    for file in get_all_filenames():
        with open('data/{}'.format(file)) as f:
            text = f.read()
            tags = tag_data(text)
            words = get_words(tags)
            bigrams = filter_bigrams(calculate_bigrams(words))
            unigrams = calculate_unigrams(words)
            for k, v in bigrams.items():
                if k in total_bigrams.keys():
                    total_bigrams[k] += v
                else:
                    total_bigrams[k] = v
            for k, v in unigrams.items():
                if k in total_unigrams.keys():
                    total_unigrams[k] += v
                else:
                    total_unigrams[k] = v
    llrs = calculate_LLR(total_unigrams, total_bigrams)
    sorted_llrs = sorted([(k, v) for (k, v) in llrs.items()
                          if k[0].split(":")[1] == "subst" and
                          k[1].split(":")[1] in ["subst", "adj", "adja", "adjp", "adjc"]],
                        key=lambda x: x[1], reverse=True)[:50]
    save_results(sorted_llrs)


if __name__ == "__main__":
    main()
