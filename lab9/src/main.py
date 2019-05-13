from src.file_utils import get_random_files
import requests


def upload_file(text):
    url = 'http://ws.clarin-pl.eu/nlprest2/base/upload/'
    a = requests.post(url, data=text.encode('utf-8'), headers={'Content-Type': 'binary/octet-stream'})
    print(a.text)


def main():
    data = get_random_files(100)
    upload_file(data[list(data.keys())[0]])


if __name__ == '__main__':
    main()
