from os import listdir


def read_file(filename):
    with open('data/{}'.format(filename), 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def get_all_filenames():
    filenames = listdir('data')
    filenames.remove('.gitkeep')
    filenames.remove('polimorfologik.txt')
    return filenames


def get_data():
    data = {}
    filenames = get_all_filenames()
    for filename in filenames:
        data[filename] = read_file(filename)
    return data


def read_polimorfologik():
    words = set()
    with open('data/polimorfologik.txt', 'r', encoding='utf-8') as file:
        for line in file:
            words.add(line.split(';')[1].lower())
    return words


def save_results(words_not_in_dict, top_words_not_in_dict, words_not_in_dict_with_3_occurrences, corrections):
    with open('results/words_not_in_dictionary.txt', 'w', encoding='utf-8') as f:
        f.write('Words not found in dictionary:\n')
        for w in words_not_in_dict:
            f.write('\t{}\n'.format(w))
    with open('results/results.txt', 'w', encoding='utf-8') as f:
        f.write('Top 30 words not found in dictionary:\n')
        for w in top_words_not_in_dict:
            f.write('\t{}\n'.format(w))
        f.write('\nTop 30 words with 3 occurences not found in dictionary:\n')
        for w in words_not_in_dict_with_3_occurrences:
            f.write('\t{}\n'.format(w))
        f.write('\nWord corrections:\n')
        for w in corrections:
            f.write('\t{} -> {}\n'.format(w[0], w[1]))
