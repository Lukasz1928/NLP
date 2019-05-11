import random
from math import ceil

import regex


def amends(title):
    try:
        _ = regex.search(r'o\s+zmianie\s+(\w*\s+)?ustaw\w*', title, regex.MULTILINE | regex.DOTALL)[0]
    except TypeError:
        return False
    return True


def split_title(text):
    title_end_index = min([x for x in [text.find('Art'), text.find('Rozdział')] if x >= 0])
    return text[:title_end_index], text[title_end_index:]


def remove_title(text):
    try:
        t, c = split_title(text)
        return c
    except ValueError:
        return None


def remove_titles(data):
    t = {k: remove_title(v) for k, v in data.items()}
    return {k: v for k, v in t.items() if v is not None}


def split_data(data):
    amending = set()
    not_amending = set()
    for name, text in data.items():
        try:
            title, _ = split_title(text)
        except ValueError:
            pass
        else:
            if amends(title):
                amending.add(name)
            else:
                not_amending.add(name)
    return amending, not_amending


def split_test_train_validation(files):
    to_be_used = files
    train = set(random.sample(to_be_used, k=int(0.6 * len(to_be_used))))
    for t in train:
        to_be_used.remove(t)
    test = set(random.sample(to_be_used, k=int(0.5 * len(to_be_used))))
    for t in test:
        to_be_used.remove(t)
    validation = to_be_used
    return test, train, validation


def get_random_lines(text, size, percentage=False):
    lines = [l for l in text.split('\n') if len(l) > 15]
    return " ".join(random.sample(lines, k=min(len(lines), ceil(size / 100.0 * len(lines)) if percentage else size)))
