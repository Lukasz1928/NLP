import json

import requests

from src.utils import get_url


def save(synonyms):
    syns = {str(k): v for k, v in synonyms.items()}
    with open('results/meanings.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(syns, indent=2, ensure_ascii=False))


def get_searched_noun_ids(word):
    words = requests.get(get_url('lexemes/{}'.format(word))).json()
    searched_noun_sense = [w['sense_id'] for w in words if w['part_of_speech'] == 'noun_pl' and w['lemma'] == word][0]
    senses = requests.get(get_url('senses/{}'.format(searched_noun_sense))).json()
    ids = [w['id'] for w in senses['homographs'] if w['part_of_speech'] == 'noun_pl']
    return ids


def get_meaning_and_synonyms(sense_id):
    senses = requests.get(get_url('senses/{}'.format(sense_id))).json()
    d = {
        'definition': senses['definition'],
        'synonyms': [(s['lemma'], s['sense_index']) for s in senses['synset']['senses'] if
                     (s['lemma'], s['sense_index']) != (senses['lemma'], senses['sense_index'])]
    }
    return (senses['lemma'], senses['sense_index']), d


def find_meanings_and_synonyms(word):
    sense_ids = get_searched_noun_ids(word)
    data = dict([get_meaning_and_synonyms(sense_id) for sense_id in sense_ids])
    save(data)
