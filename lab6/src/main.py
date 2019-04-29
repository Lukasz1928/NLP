from src.meanings import find_meanings_and_synonyms
from src.hypernymy import find_hypernymy_relation_closure


def main():
    # find_meanings_and_synonyms('szkoda')
    find_hypernymy_relation_closure('wypadek drogowy')


if __name__ == "__main__":
    main()
