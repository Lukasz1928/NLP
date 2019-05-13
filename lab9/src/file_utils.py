import random
from os import listdir


def read_file(filename):
    with open('data/{}'.format(filename), 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def get_all_filenames():
    filenames = listdir('data')
    filenames.remove('.gitkeep')
    return filenames


def get_random_filenames(cnt):
    filenames = get_all_filenames()
    return random.sample(filenames, k=cnt)


def get_random_files(cnt):
    data = {}
    filenames = get_random_filenames(cnt)
    for filename in filenames:
        data[filename] = read_file(filename)
    return data
