from src.meanings import find_meanings_and_synonyms
from src.hypernymy import find_hypernymy_relation_closure
from src.hyponyms import find_hyponyms


def main():
    # find_meanings_and_synonyms('szkoda')
    # find_hypernymy_relation_closure('wypadek drogowy')
    find_hyponyms('wypadek', 1)

if __name__ == "__main__":
    main()
