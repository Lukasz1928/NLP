import requests


def start_processing_file(text):
    url = 'http://ws.clarin-pl.eu/nlprest2/base/startTask'
    a = requests.post(url, data=text.encode('utf-8'), headers={'Content-Type': 'binary/octet-stream'})
    print(a.text)
