from src.file_utils import get_random_files
from src.ner import start_processing_file, get_status, get_result, get_processed


def main():
    data = get_random_files(2)
    upload_ids = [start_processing_file(text) for name, text in data.items()]
    named = get_processed(upload_ids)
    print(named[0])


if __name__ == '__main__':
    main()
