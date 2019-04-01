## Tasks

1. Use ElasticSearch term vectors API to retrieve and store for each document the following data:
   1. The terms (tokens) that are present in the document.
   2. The number of times given term is present in the document.
1. Aggregate the result to obtain one global **frequency list**.
1. Filter the list to keep terms that contain only letters and have at least 2 of them.
1. Make a plot in a logarithmic scale:
   1. X-axis should contain the **rank** of a term, meaning the first rank belongs to the term with the highest number of
      occurrences; the terms with the same number of occurrences should be ordered by their name,
   2. Y-axis should contain the **number of occurrences** of the term with given rank.
1. Download [polimorfologik.zip](https://github.com/morfologik/polimorfologik/releases/download/2.1/polimorfologik-2.1.zip) dictionary
   and use it to find all words that do not appear in that dictionary.
1. Find 30 words with the highest ranks that do not belong to the dictionary.
1. Find 30 words with 3 occurrences that do not belong to the dictionary.
1. Use Levenshtein distance and the frequency list, to determine the most probable correction of the words from the
   second list.