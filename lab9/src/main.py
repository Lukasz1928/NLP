from src.file_utils import get_random_files
from src.ner import start_processing_file, get_status, get_result, get_processed
from src.xml_parser import parse_xml


def main():
    data = get_random_files(100)
    upload_ids = [start_processing_file(text) for name, text in data.items()]
    print('upload complete')
    named = get_processed(upload_ids)
    i = 0
    for n in named:
        with open('data/parsed/{}.xml'.format(i), 'w+', encoding='utf-8') as f:
            f.write(n)
    # with open('src/r.xml', 'r', encoding='utf-8') as f:
    #     named = [f.read()]
    # parsed = [parse_xml(n) for n in named]


if __name__ == '__main__':
    main()
