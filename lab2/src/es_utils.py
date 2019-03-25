from elasticsearch import NotFoundError
from src.file_utils import get_data


def create_index(es, index_name):
    index = {
        'settings': {
            'analysis': {
                'filter': {
                    'synonym': {
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
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': ['lowercase', 'synonym', 'morfologik_stem'],
                    }
                }
            },
        },
        'mappings': {
            'doc': {
                'properties': {
                    'text': {
                        'type': 'text',
                        'analyzer': 'myanalyzer'
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
    for k, v in data.items():
        es.create(index_name, doc_type='doc', id=k, body={'text': v})
    es.indices.refresh(index_name)


def clean_up(es, index_name):
    try:
        es.indices.delete(index_name)
    except NotFoundError:
        pass
