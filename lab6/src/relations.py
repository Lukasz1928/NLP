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
    if senses['language'] != 'pl_PL':
        return None, None
    rels_out = senses['outgoing']
    rels_in = senses['incoming']
    for r in rels_in:
        relation = get_relation(r['relation_id'])
        if relation in ['hiponimia', 'hiperonimia']:
            for s in r['senses']:
                rels.add((s['id'], word_id))
                labels[(s['id'], word_id)] = relation
    for r in rels_out:
        relation = get_relation(r['relation_id'])
        if relation in ['hiponimia', 'hiperonimia']:
            for s in r['senses']:
                rels.add((word_id, s['id']))
                labels[(word_id, s['id'])] = relation
    return rels, labels


def get_word_id(word, word_id, part_of_speech='noun_pl'):
    words = requests.get(get_url('lexemes/{}'.format(word))).json()
    if part_of_speech is None:
        searched_sense = [w['sense_id'] for w in words if w['lemma'] == word][0]
    else:
        searched_sense = [w['sense_id'] for w in words if w['part_of_speech'] == 'noun_pl' and w['lemma'] == word][0]
    senses = requests.get(get_url('senses/{}'.format(searched_sense))).json()
    if word_id is None:
        if part_of_speech is None:
            ids = [w['id'] for w in senses['homographs']]
        else:
            ids = [w['id'] for w in senses['homographs'] if w['part_of_speech'] == 'noun_pl']
    else:
        if part_of_speech is None:
            ids = [w['id'] for w in senses['homographs'] if w['sense_index'] == word_id]
        else:
            ids = [w['id'] for w in senses['homographs'] if w['part_of_speech'] == 'noun_pl' and w['sense_index'] == word_id]
    return ids


def find_relations_in_group(words, name):
    word2id = {w: None for w in words}
    id2word = {}
    for w in words:
        try:
            word_id = get_word_id(w[0], word_id=w[1], part_of_speech=None)[0]
        except IndexError:
            pass
        else:
            word2id[w] = word_id
            id2word[word_id] = w
    graph_vertices = set(words)
    graph_edges = []
    edge_labels = {}

    for w in id2word.values():
        rels, labels = get_word_relations(word2id[w])
        for r in rels:
            if r[0] in word2id.values() and r[1] in word2id.values():
                named_r = (id2word[r[0]], id2word[r[1]])
                graph_edges.append(named_r)
                edge_labels[named_r] = labels[r]

    g = networkx.MultiDiGraph()
    g.add_nodes_from(graph_vertices)
    g.add_edges_from(graph_edges)
    pos = networkx.circular_layout(g)
    plt.subplot(121)
    networkx.draw(g, pos, edge_labels=edge_labels, with_labels=True, font_size=6)
    networkx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, with_labels=True, font_size=6)
    plt.xlim(1.2 * min([x for x, y in pos.values()]), 1.2 * max([x for x, y in pos.values()]))
    plt.ylim(1.2 * min([y for x, y in pos.values()]), 1.2 * max([y for x, y in pos.values()]))
    plt.savefig('results/{}.png'.format(name))
    plt.clf()