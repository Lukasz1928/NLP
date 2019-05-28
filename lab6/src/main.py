from src.meanings import find_meanings_and_synonyms
from src.hypernymy import find_hypernymy_relation_closure
from src.hyponyms import find_direct_hyponyms, find_second_order_hyponyms
from src.relations import find_relations_in_group
from src.similarity import calculate_lch


def main():
    find_meanings_and_synonyms('szkoda')  # task 3
    find_hypernymy_relation_closure('wypadek drogowy')  # task 4
    find_direct_hyponyms('wypadek', 1)  # task 5
    find_second_order_hyponyms('wypadek', 1)  # task 6
    find_relations_in_group([('szkoda', 2), ('strata', 1), ('szkoda majątkowa', 1), ('uszczerbek na zdrowiu', 1),
                             ('krzywda', 1), ('niesprawiedliwość', 1), ('nieszczęście', 2)], "group1")  # task 7i
    find_relations_in_group([('wypadek', 1), ('wypadek komunikacyjny', 1), ('kolizja', 2),
                             ('zderzenie', 2), ('kolizja drogowa', 1), ('bezkolizyjny', 2),
                             ('katastrofa budowlana', 1), ('wypadek drogowy', 1)], "group2")  # task 7ii
    calculate_lch([(('szkoda', 2), ('wypadek', 1)),
                   (('kolizja', 2), ('szkoda majątkowa', 1)),
                   (('nieszczęście', 2), ('katastrofa budowlana', 1))])  # task 8


if __name__ == "__main__":
    main()
