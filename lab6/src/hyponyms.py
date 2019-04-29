import requests
from src.meanings import get_searched_noun_ids
from src.utils import get_url


def save(hyponyms, description, reset_file=True):
    with open('results/hyponyms.txt', 'w+' if reset_file else 'a+', encoding='utf-8') as f:
        f.write(description)
        for h in hyponyms:
            f.write('\t{}\n'.format(h))


def get_hyponyms(sense_id):
    s = requests.get(get_url('senses/{}'.format(sense_id))).json()
    hyponyms_data = [x for x in s['outgoing'] if x['relation_id'] == 10]
    if len(hyponyms_data) == 0:
        return []
    hyponyms = [(x['lemma'], x['sense_index']) for x in hyponyms_data[0]['senses']]
    return hyponyms


def get_first_order_hyponyms(word, word_id):
    sense_id = get_searched_noun_ids(word, word_id)[0]
    h = get_hyponyms(sense_id)
    return h


def find_direct_hyponyms(word, word_id):
    h = get_first_order_hyponyms(word, word_id)
    save(h, 'Direct hyponyms of {} word:\n'.format((word, word_id)))


def find_second_order_hyponyms(word, word_id):
    first_order_hyponyms = get_first_order_hyponyms(word, word_id)
    second_order_hyponyms = set()
    for foh in first_order_hyponyms:
        for h in get_first_order_hyponyms(*foh):
            second_order_hyponyms.add(h)
    save(second_order_hyponyms, '\nSecond order hyponyms of {} word:\n'.format((word, word_id)), reset_file=False)
