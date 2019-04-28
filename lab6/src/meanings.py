import json

import requests

from src.utils import get_url


def get_synonyms(synset_id):
    senses = requests.get(get_url('synsets/{}/senses'.format(synset_id))).json()
    synonyms = [(syn['lemma']['word'], syn['senseNumber']) for syn in senses]
    return synonyms


def get_meaning(synset_id):
    attrs = requests.get(get_url('synsets/{}/attributes'.format(synset_id))).json()
    meaning_attr = None
    for attr in attrs:
        try:
            if attr['type']['tableName'] == 'sense':
                meaning_attr = attr['value']
        except KeyError:
            pass  # ignore - no definition provided for synset
    return meaning_attr


def save(synonyms):
    syns = {str(k): v for k, v in synonyms.items()}
    with open('results/meanings.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(syns, indent=4))


def find_meanings_and_synonyms(word):
    senses = requests.get(get_url('senses/search?lemma={}&partOfSpeech={}'.format(word, 'noun'))).json()['content']
    senses_ids = [s['id'] for s in senses]
    synsets_ids = [requests.get(get_url('senses/{}/synset'.format(i))).json()['id'] for i in senses_ids]
    meanings_list = [{'synonyms': get_synonyms(i), 'meaning': get_meaning(i)} for i in synsets_ids]
    meanings = {}
    for m in meanings_list:
        for s in m['synonyms']:
            if s[0] == word:
                m['synonyms'].remove(s)
                meanings[s] = m
    save(meanings)
