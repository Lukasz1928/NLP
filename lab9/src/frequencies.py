import matplotlib.pyplot as plt


def calculate_frequencies(parsed):
    freqs = {}
    for doc in parsed:
        for chunk in doc:
            for sentence in chunk:
                sentence_freqs = {}
                for token in sentence:
                    for cls in token[1]:
                        if cls[0] not in sentence_freqs or sentence_freqs[cls[0]] < cls[1]:
                            sentence_freqs[cls[0]] = cls[1]
                for k, v in sentence_freqs.items():
                    if k in freqs:
                        freqs[k] += v
                    else:
                        freqs[k] = v
    return freqs


def calculate_coarse_frequencies(frequencies):
    coarse_frequencies = {}
    for k, v in frequencies.items():
        coarse_key = '_'.join(k.split('_')[:2])
        if coarse_key in coarse_frequencies.keys():
            coarse_frequencies[coarse_key] += v
        else:
            coarse_frequencies[coarse_key] = v
    return coarse_frequencies


def plot_frequencies(frequencies, label, title, filename):
    xs = sorted(list(frequencies.keys()), key=lambda k: frequencies[k], reverse=True)
    ys = [frequencies[x] for x in xs]
    plt.bar(xs, ys)
    plt.xticks(rotation=90)
    plt.ylabel(label)
    plt.title(title)
    plt.tight_layout()
    plt.savefig('results/{}.png'.format(filename))
    plt.clf()


def calculate_most_frequent(parsed):
    class_entities = {}
    for doc in parsed:
        for chunk in doc:
            for sentence in chunk:
                classes = set()
                for token in sentence:
                    for cls in token[1]:
                        if cls[1] > 0:
                            classes.add(cls)
                phrases_for_class = {}
                for token in sentence:
                    for cls in classes:
                        if cls in token[1]:
                            if cls in phrases_for_class.keys():
                                phrases_for_class[cls].append(token[0])
                            else:
                                phrases_for_class[cls] = [token[0]]
                for k in phrases_for_class:
                    phrases_for_class[k] = ' '.join(phrases_for_class[k])
                for k, v in phrases_for_class.items():
                    if k in class_entities.keys():
                        class_entities[k].append(v)
                    else:
                        class_entities[k] = [v]
    entities_with_frequencies = {k: sorted(list(set([(x, v.count(x)) for x in v])), key=lambda x: x[1], reverse=True)
                                 for k, v in class_entities.items()}
    return calculate_total_frequencies(entities_with_frequencies), calculate_frequencies_per_class(
        entities_with_frequencies)


def calculate_total_frequencies(ewf):
    f = {}
    for v in ewf.values():
        for w in v:
            if w[0] in f.keys():
                f[w[0]] += w[1]
            else:
                f[w[0]] = w[1]
    freqs = sorted([(k, v) for k, v in f.items()], key=lambda x: x[1], reverse=True)[:50]
    return freqs


def merge_freqs(d1, d2):
    s1 = {k: v for (k, v) in d1}
    s2 = {k: v for (k, v) in d2}
    s12 = {k: 0 for k in list(s1.keys()) + list(s2.keys())}
    for k, v in d1:
        s12[k] += v
    for k, v in d2:
        s12[k] += v
    return [(k, v) for k, v in s12.items()]


def to_coarse_classes(ewf):
    f = {}
    for k, v in ewf.items():
        coarse_key = '_'.join(k[0].split('_')[:2])
        if coarse_key in f.keys():
            f[coarse_key] = merge_freqs(f[coarse_key], v)
        else:
            f[coarse_key] = v
    return f


def calculate_frequencies_per_class(ewf):
    freqs = to_coarse_classes(ewf)
    for k in freqs:
        freqs[k] = sorted(freqs[k], key=lambda x: x[1], reverse=True)[:10]
    return freqs
