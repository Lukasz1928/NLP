## Tasks

1. Download [docker image](https://hub.docker.com/r/djstrong/krnnt2) o KRNNT2. It includes the following tools:
   1. Morfeusz2 - morphological dictionary
   1. Corpus2 - corpus access library
   1. Toki - tokenizer for Polish
   1. Maca - morphosyntactic analyzer
   1. rknnt - Polish tagger
1. Use the tool to tag and lemmatize the corpus with the bills.
1. Using the tagged corpus compute bigram statistic for the tokens containing:
   1. lemmatized, downcased word
   1. morphosyntactic category of the word (noun, verb, etc.)
1. Exclude bigram containing non-words (such as numbers, interpunction, etc.)
1. For example: "Ala ma kota", which is tagged as:
   ```
   Ala	none
           Ala	subst:sg:nom:f	disamb
   ma	space
           mieć	fin:sg:ter:imperf	disamb
   kota	space
           kot	subst:sg:acc:m2	disamb
   .	none
           .	interp	disamb
   ```
   the algorithm should return the following bigrams: `ala:subst mieć:fin` and `mieć:fin kot:subst`.
1. Compute LLR statistic for this dataset.
1. Select top 50 results including noun at the first position and noun or adjective at the second position.