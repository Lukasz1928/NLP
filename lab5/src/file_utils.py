from os import listdir


def read_file(filename):
    with open('../data/{}'.format(filename), 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def get_all_filenames():
    filenames = listdir('../data')
    filenames.remove('.gitkeep')
    return filenames


def get_data():
    data = {}
    filenames = get_all_filenames()
    for filename in filenames:
        data[filename] = read_file(filename)
    return data


def save_results():
    pass
