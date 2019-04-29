import requests
from src.meanings import get_searched_noun_ids
from src.utils import get_url


def save(word, word_id, hyponyms):
    with open('results/hyponyms.txt', 'w', encoding='utf-8') as f:
        f.write('Direct hyponyms of {} word:\n'.format((word, word_id)))
        for h in hyponyms:
            f.write('\t{}\n'.format(h))


def get_hyponyms(sense_id):
    s = requests.get(get_url('senses/{}'.format(sense_id))).json()
    hyponyms_data = [x for x in s['outgoing'] if x['relation_id'] == 10][0]
    hyponyms = [(x['lemma'], x['sense_index']) for x in hyponyms_data['senses']]
    return hyponyms


def find_hyponyms(word, word_id):
    sense_id = get_searched_noun_ids(word, word_id)[0]
    h = get_hyponyms(sense_id)
    save(word, word_id, h)