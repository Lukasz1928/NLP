from src.file_utils import get_random_files
from src.ner import upload_file


def main():
    data = get_random_files(100)
    upload_file(data[list(data.keys())[0]])


if __name__ == '__main__':
    main()
