from elasticsearch import NotFoundError
from src.file_utils import get_data


def create_index(es, index_name):
    index = {
        'settings': {
            'analysis': {
                'filter': {
                    'myfilter': {
                        'type': 'synonym',
                        'synonyms': [
                            "kpk => kodeks postępowania karnego",
                            "kpc => kodeks postępowania cywilnego",
                            "kk => kodeks karny",
                            "kc => kodeks cywilny"]
                    }
                },
                'analyzer': {
                    'myanalyzer': {
                        'tokenizer': 'standard',
                        'filter': ['myfilter', 'lowercase']
                    }
                }
            },
        },
        'mappings': {
            'doc': {
                'properties': {
                    'content': {
                        'type': 'text',
                        'analyzer': 'morfologik'
                    }
                }
            }
        }
    }
    try:
        es.indices.delete(index_name)
    except NotFoundError:
        pass  # just to make sure that index does not exist
    es.indices.create(index_name, index)


def load_data(es, index_name):
    data = get_data()
    for i, k in enumerate(data.keys()):
        es.create(index_name, doc_type='doc', id=i, body={'content': data[k]})


def clean_up(es, index_name):
    try:
        es.indices.delete(index_name)
    except NotFoundError:
        pass