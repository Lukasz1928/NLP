import math
from collections import deque

from src.meanings import get_meaning_and_synonyms
from src.relations import get_word_id, get_word_relations


def distance(w1, w2):
    id1 = get_word_id(*w1)[0]
    id2 = get_word_id(*w2)[0]
    queue = deque([id1])
    waiting = {id1}
    done = set()
    dist = {id1: 0}
    while len(queue) > 0:
        w = queue.popleft()
        waiting.remove(w)
        if w not in done:
            done.add(w)
            rels, labels = get_word_relations(w)
            if rels is None:
                continue
            for r in rels:
                rel_id = r[0 if r[1] == w else 1]
                if rel_id not in done:
                    dist[rel_id] = dist[w] + 1
                    if rel_id not in waiting:
                        queue.append(rel_id)
                        waiting.add(rel_id)
                if rel_id == id2:
                    return dist[rel_id]
    return -1


def lch(w1, w2):
    depth = 12  # that's just an assumption
    d = distance(w1, w2)
    try:
        lch_distance = -math.log(d / (2 * depth))
    except ValueError:
        lch_distance = 'inf'
    return lch_distance


def calculate_lch(word_pairs):
    r = {}
    for w in word_pairs:
        r[w] = lch(*w)
        print(r[w])
    with open('results/similarity.txt', 'w+', encoding='utf-8') as f:
        f.write('Leacock-Chodorow similarity measure:\n')
        for w in word_pairs:
            f.write('{}, {} -> {}'.format(w[0], w[1], r[w]))
