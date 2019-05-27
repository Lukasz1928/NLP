from src.meanings import find_meanings_and_synonyms
from src.hypernymy import find_hypernymy_relation_closure
from src.hyponyms import find_direct_hyponyms, find_second_order_hyponyms
from src.relations import find_relations_in_group, get_word_id, get_word_relations


def main():
    # a = get_word_id('kolizja', 2)[0]
    # print(get_word_id('bezkolizyjny', 2, None))
    # print(get_word_relations(a))
    # exit()

    # find_meanings_and_synonyms('szkoda')  # task 3
    # find_hypernymy_relation_closure('wypadek drogowy')  # task 4
    # find_direct_hyponyms('wypadek', 1)  # task 5
    # find_second_order_hyponyms('wypadek', 1)  # task 6
    # find_relations_in_group([('szkoda', 2), ('strata', 1), ('szkoda majątkowa', 1), ('uszczerbek na zdrowiu', 1),
    #                          ('krzywda', 1), ('niesprawiedliwość', 1), ('nieszczęście', 2)], "group1") # task 7i
    find_relations_in_group([('wypadek', 1), ('wypadek komunikacyjny', 1), ('kolizja', 2),
                             ('zderzenie', 2), ('kolizja drogowa', 1), ('bezkolizyjny', 2),
                             ('katastrofa budowlana', 1), ('wypadek drogowy', 1)], "group2") # task 7ii


if __name__ == "__main__":
    main()
