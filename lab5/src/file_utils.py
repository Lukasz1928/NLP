from os import listdir


def get_all_filenames():
    filenames = listdir('data')
    filenames.remove('.gitkeep')
    print(filenames)
    return filenames


def save_results(llrs):
    with open('results/results.txt', 'w', encoding='utf-8') as f:
        for (k, v) in llrs:
            f.write('{} -> {}\n'.format(k, v))
