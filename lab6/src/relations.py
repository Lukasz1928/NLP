import networkx
import requests
import matplotlib.pyplot as plt
from src.utils import get_url


def get_relation(rel_id):
    r = requests.get('http://graph-slowosiec.clarin-pl.eu/wordnetloom/resources/relation-types/{}'.format(rel_id)).json()
    return r['name']


def get_word_relations(word_id):
    rels = set()
    labels = {}
    senses = requests.get(get_url('senses/{}'.format(word_id))).json()
    rels_out = senses['outgoing']
    rels_in = senses['incoming']
    for r in rels_in:
        relation = get_relation(r['relation_id'])
        for s in r['senses']:
            rels.add((s['id'], word_id))
            labels[(s['id'], word_id)] = relation
    return rels, labels


def get_word_id(word, word_id):
    words = requests.get(get_url('lexemes/{}'.format(word))).json()
    searched_sense = [w['sense_id'] for w in words if w['part_of_speech'] == 'noun_pl' and w['lemma'] == word][0]
    senses = requests.get(get_url('senses/{}'.format(searched_sense))).json()
    if word_id is None:
        ids = [w['id'] for w in senses['homographs'] if w['part_of_speech'] == 'noun_pl']
    else:
        ids = [w['id'] for w in senses['homographs'] if w['part_of_speech'] == 'noun_pl' and w['sense_index'] == word_id]
    return ids


def find_relations_in_group(words):
    word2id = {}
    id2word = {}
    for w in words:
        word_id = get_word_id(w[0], word_id=w[1])
        word2id[w] = word_id
        id2word[word_id] = w

    graph_vertices = set(words)
    graph_edges = set()
    edge_labels = {}

    for w in words:
        rels, labels = get_word_relations(word2id[w])
        for r in rels:
            if r[1] in word2id.values():
                graph_edges.add(r)
                edge_labels[r] = labels[r]

    g = networkx.DiGraph()
    g.add_node(graph_vertices)
    plt.subplot(121)
    networkx.draw(g, with_labels=True, font_size=8)
    plt.show()