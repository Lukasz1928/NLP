## Tasks

1. Install ElasticSearch (ES).
1. Install an ES plugin for Polish https://github.com/allegro/elasticsearch-analysis-morfologik 
1. Define an ES analyzer for Polish texts containing:
   1. standard tokenizer
   1. synonym filter with the following definitions:
      1. kpk - kodeks postępowania karnego
      1. kpc - kodeks postępowania cywilnego
      1. kk - kodeks karny
      1. kc - kodeks cywilny
   1. Morfologik-based lemmatizer
   1. lowercase filter
1. Define an ES index for storing the contents of the legislative acts.
1. Load the data to the ES index.
1. Determine the number of legislative acts containing the word **ustawa** (in any form).
1. Determine the number of legislative acts containing the words **kodeks postępowania cywilnego** 
   in the specified order, but in an any inflection form.
1. Determine the number of legislative acts containing the words **wchodzi w życie** 
   (in any form) allowing for up to 2 additional words in the searched phrase.
1. Determine the 10 documents that are the most relevant for the phrase **konstytucja**.
1. Print the excerpts containing the word **konstytucja** (up to three excerpts per document) 
   from the previous task.