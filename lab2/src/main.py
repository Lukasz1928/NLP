import elasticsearch
from src.es_utils import create_index, load_data, clean_up


def count_acts_with_word_ustawa(es, index_name):
    search_body = {
        'query': {
            'match': {
                'text': {
                    'query': 'ustawa'
                }
            }
        }
    }
    ret = es.search(index=index_name, doc_type='doc', body=search_body)
    count = ret['hits']['total']
    return count


def count_acts_with_kpc(es, index_name):
    search_body = {
        'query': {
            'match_phrase': {
                'text': {
                    'query': 'kodeks postępowania cywilnego'
                }
            }
        }
    }
    ret = es.search(index=index_name, doc_type='doc', body=search_body)
    count = ret['hits']['total']
    return count


def count_acts_with_wchodzi_w_zycie(es, index_name):
    search_body = {
        'query': {
            'match_phrase': {
                'text': {
                    'query': 'wchodzi w życie',
                    'slop': 2
                }
            }
        }
    }
    ret = es.search(index=index_name, doc_type='doc', body=search_body)
    count = ret['hits']['total']
    return count


def find_documents_most_relevant_for_konstytucja(es, index_name):
    search_body = {
        'size': 10,
        'query': {
            'match': {
                'text': {
                    'query': 'konstytucja'
                }
            }
        }
    }
    ret = es.search(index=index_name, doc_type='doc', body=search_body)
    print(ret)
    hits = ret['hits']['hits']
    return [h['_id'] for h in hits]


def get_excerpts_with_konstytucja(es, index_name):
    search_body = {
        'size': 10,
        'query': {
            'match': {
                'text': {
                    'query': 'konstytucja'
                }
            }
        },
        'highlight': {
            'fields': {
                'text': {}
            },
            'number_of_fragments': 3
        }
    }
    ret = es.search(index=index_name, doc_type='doc', body=search_body)
    hits = ret['hits']['hits']
    return [(h['_id'], h['highlight']['text']) for h in hits]


def solve_tasks(es, index_name, output_name):
    with open('results/{}.txt'.format(output_name), 'w+', encoding='utf-8') as f:
        f.write('Acts containing word \'ustawa\' in any form: {}\n\n'
                .format(count_acts_with_word_ustawa(es, index_name)))
        f.write('Acts containing words \'kodeks postępowania cywilnego\': {}\n\n'
                .format(count_acts_with_kpc(es, index_name)))
        f.write('Acts containing words \'wchodzi w życie\' with up to 2 additional words: {}\n\n'
                .format(count_acts_with_wchodzi_w_zycie(es, index_name)))
        f.write('Documents most relevant for \'konstytucja\': \n\n')
        for doc in find_documents_most_relevant_for_konstytucja(es, index_name):
            f.write('\t{}\n'.format(doc))
        f.write('\nExcerpts containing word \'konstytucja\':\n')
        for doc in get_excerpts_with_konstytucja(es, index_name):
            f.write('\t{}:\n'.format(doc[0]))
            for t in doc[1]:
                f.write('\t\t\'{}\'\n'.format(t))



def main():
    index_name = 'idx'
    es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
    #create_index(es, index_name)
    #load_data(es, index_name)
    solve_tasks(es, index_name, "result")
    #clean_up(es, index_name)


if __name__ == "__main__":
    main()
