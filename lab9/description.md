## Tasks

1. Read the classification of [Named Entities](http://clarin-pl.eu/pliki/warsztaty/Wyklad3-inforex-liner2.pdf).
1. Read the [API of NER](http://nlp.pwr.wroc.pl/redmine/projects/nlprest2/wiki) in [Clarin](http://ws.clarin-pl.eu/ner.shtml).
1. Read the [documentation of CLL format](http://nlp.pwr.wroc.pl/redmine/projects/corpus2/wiki/CCL_format).
1. Randomly select 100 bills.
1. Recognize the named entities in the documents using the `n82` model.
1. Plot the frequency of the recognized classes:
   1. fine-grained classification histogram (classes such as `nam_fac_bridge`, `nam_liv_animal`).
   1. coarse-grained classification histogram (classes such as `nam_adj`, `nam_eve`, `nam_fac`).
1. Display 50 most frequent Named Entities including their count and fine-grained type.
1. Display 10 most frequent Named Entities for each coarse-grained type.
1. Discuss the results of the extraction.