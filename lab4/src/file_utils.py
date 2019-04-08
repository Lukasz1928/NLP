from os import listdir


def read_file(filename):
    with open('data/{}'.format(filename), 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def get_all_filenames():
    filenames = listdir('data')
    filenames.remove('.gitkeep')
    return filenames


def get_data():
    data = {}
    filenames = get_all_filenames()
    for filename in filenames:
        data[filename] = read_file(filename)
    return data


def save_results(bigrams, pmis, llrs):
    with open('results/bigrams.txt', 'w', encoding='utf-8') as f:
        for b in sorted(bigrams.items(), key=lambda b: b[1], reverse=True)[:30]:
            f.write('{}\n'.format(b))
    with open('results/results.txt', 'w', encoding='utf-8') as f:
        f.write('Top bigrams by PMI:\n')
        for p in pmis:
            f.write('\t{}, {}\n'.format(p[0], p[1]))
        f.write('\nTop bigrams by LLR:\n')
        for l in llrs:
            f.write('\t{}, {}\n'.format(l[0], l[1]))