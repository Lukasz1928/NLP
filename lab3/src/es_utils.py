from elasticsearch import NotFoundError
from src.file_utils import get_data


def create_index(es, index_name):
    index = {
        "settings": {
            "analysis": {
                "filter": ["lowercase"]
            }
        },
        "mappings": {
            "doc": {
                "properties": {
                    "text": {
                        "type": "text",
                        "term_vector": "yes",
                        "store": 'true'
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
