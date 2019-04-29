import regex

import requests
import networkx

from src.utils import get_url
import matplotlib.pyplot as plt


def get_id(word):
    words = requests.get(get_url('lexemes/{}'.format(word))).json()
    searched_noun_sense = [w['sense_id'] for w in words][0]
    sense = requests.get(get_url('senses/{}'.format(searched_noun_sense))).json()
    return sense['id']


def id_to_word(word_id):
    sense = requests.get(get_url('senses/{}'.format(word_id))).json()
    return regex.sub(r'\s+', r'\n', sense['lemma'])


def get_hypernyms(word_id):
    sense = requests.get(get_url('senses/{}'.format(word_id))).json()
    try:
        hypernyms = [h['senses'] for h in sense['incoming'] if h['language'] == 'pl_PL' and h['relation_id'] == 10][0]
    except IndexError:
        hypernyms = []
    return [h['id'] for h in hypernyms]


def find_relation(word_id):
    rel = set()
    to_find = [word_id]
    while len(to_find) > 0:
        elem = to_find.pop()
        hyps = get_hypernyms(elem)
        for h in hyps:
            rel.add((elem, h))
            to_find.append(h)
    return rel


def find_relation_closure(rel):
    crel = set([x for x in rel])
    added = True
    while added:
        added = False
        to_add = set()
        for (a, b) in crel:
            for (c, d) in crel:
                if b == c and (a, d) not in crel and (a, d) not in to_add:
                    to_add.add((a, d))
                    added = True
        crel.update(to_add)
    return crel


def draw_graph(rel):
    g = networkx.DiGraph()
    g.add_nodes_from(set([x[0] for x in rel] + [x[1] for x in rel]))
    g.add_edges_from(rel)
    plt.subplot(121)
    networkx.draw(g, with_labels=True, font_size=8)
    plt.savefig('results/hypernymy.png')


def find_hypernymy_relation_closure(word):
    word_id = get_id(word)
    rel = find_relation(word_id)
    word_rel = set([(id_to_word(x[0]), id_to_word(x[1])) for x in rel])
    crel = find_relation_closure(word_rel)
    draw_graph(crel)
