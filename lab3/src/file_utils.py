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
    words = []
    with open('data/polimorfologik.txt', 'r', encoding='utf-8') as file:
        words.append(file.readline().split(';')[1])
    return words


def save_results(words_not_in_dict, top_words_not_in_dict, words_not_in_dict_with_3_occurences, corrections):
    pass