from src.meanings import find_meanings_and_synonyms
from src.hypernymy import find_hypernymy_relation_closure
from src.hyponyms import find_direct_hyponyms, find_second_order_hyponyms
from src.relations import find_relations_in_group


def main():
    # find_meanings_and_synonyms('szkoda')  # task 3
    # find_hypernymy_relation_closure('wypadek drogowy')  # task 4
    # find_direct_hyponyms('wypadek', 1)  # task 5
    # find_second_order_hyponyms('wypadek', 1)  # task 6
    find_relations_in_group([('szkoda', 2), ('starata', 1), ('szkoda majątkowa', 1), ('uszczerbek na zdrowiu', 1),
                             ('krzywda', 1), ('niesprawiedliwość', 1), ('nieszczęście', 2)])


if __name__ == "__main__":
    main()
