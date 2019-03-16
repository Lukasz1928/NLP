from os import listdir


def read_file(filename):
    with open('data/{}'.format(filename), 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def get_all_filenames():
    filenames = listdir('data')
    filenames.remove('.gitkeep')
    return ["1993_599.txt"]


def get_data():
    data = []
    filenames = get_all_filenames()
    for filename in filenames:
        data.append(read_file(filename))
    return data


def pprint(data):
    print('[')
    for d in data:
        print("\n{}".format(d))
    print(']')
