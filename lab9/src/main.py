from os import listdir

from src.file_utils import get_random_files
from src.frequencies import calculate_frequencies, plot_frequencies, calculate_coarse_frequencies, \
    calculate_most_frequent
from src.ner import start_processing_file, get_processed
from src.xml_parser import parse_xml


def main():
    data = get_random_files(100)
    upload_ids = [start_processing_file(text) for name, text in data.items()]
    named = get_processed(upload_ids)
    # filenames = list(listdir('data/parsed'))
    # named = []
    # for file in filenames:
    #     with open('data/parsed/{}'.format(file), 'r', encoding='utf-8') as f:
    #         named.append(f.read())
    parsed = [parse_xml(n) for n in named]

    # frequencies of classes
    frequencies = calculate_frequencies(parsed)
    plot_frequencies(frequencies, 'occurrences', 'fine-grained class frequencies', 'fine')
    coarse_frequencies = calculate_coarse_frequencies(frequencies)
    plot_frequencies(coarse_frequencies, 'occurrences', 'fine-grained class frequencies', 'coarse')

    # most frequent phrases
    total_frequencies, class_frequencies = calculate_most_frequent(parsed)
    with open('results/results.txt', 'w+', encoding='utf-8') as f:
        f.write('Most frequent named entities:\n')
        for t in total_frequencies:
            f.write('\t{}\n'.format(t))
        f.write('\nMost frequent named entities in each class:\n')
        for k, v in class_frequencies.items():
            f.write('\t{}:\n'.format(k))
            for _v in v:
                f.write('\t\t{}\n'.format(_v))


if __name__ == '__main__':
    main()
