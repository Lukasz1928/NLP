import json
import time

import requests

user = ''  # TODO: remove!!!


def start_processing_file(text):
    url = 'http://ws.clarin-pl.eu/nlprest2/base/startTask'
    resp = requests.post(url, data=json.dumps({'text': text, 'lpmn': 'any2txt|wcrft2|liner2({"model":"n82"})',
                                               'user': user}), headers={'Content-Type': 'application/json'})
    return resp.text


def get_status(task_id):
    url = 'http://ws.clarin-pl.eu/nlprest2/base/getStatus/{}'.format(task_id)
    resp = requests.get(url)
    resp_json = resp.json()
    return resp_json['status'], resp_json['value'][0]['fileID'] if resp_json['status'] == 'DONE' else None


def get_result(fileID):
    url = 'http://ws.clarin-pl.eu/nlprest2/base/download{}'.format(fileID)
    resp = requests.get(url).text
    return resp


def get_processed(upload_ids):
    waiting = set(upload_ids)
    results = []
    time.sleep(10)  # wait for data to be processed
    while len(waiting) > 0:
        done = set()
        for i in waiting:
            s, r = get_status(i)
            if s == 'DONE':
                done.add(i)
                results.append(get_result(r))
        for d in done:
            waiting.remove(d)
        time.sleep(2)
        print(len(waiting))
    return results
