from elasticsearch import Elasticsearch


def main():
    es = Elasticsearch({'host': 'localhost', 'port': 9200})


if __name__ == "__main__":
    main()
