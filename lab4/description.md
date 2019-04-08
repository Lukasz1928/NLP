## Tasks

1. Compute **bigram** counts in the corpora, ignoring bigrams which contain at least one token that is not a word
   (it contains characters other than letters). The text has to be properly normalized before the counts are computed:
   it should be downcased and all punctuation should be removed. Given the sentence: "The quick brown fox jumps over the
   lazy dog", the bigram counts are as follows:
   1. "the quick": 1
   1. "quick brown": 1
   1. "brown fox": 1
   1. etc.
1. Use [pointwise mutual information](https://en.wikipedia.org/wiki/Pointwise_mutual_information) to compute the measure 
   for all pairs of words. 
1. Sort the word pairs according to that measure in the descending order and display 30 top results.
1. Use [log likelihood ratio](http://tdunning.blogspot.com/2008/03/surprise-and-coincidence.html) (LLR) to compute the measure
   for all pairs of words.
1. Sort the word pairs according to that measure in the descending order and display 30 top results.
1. Answer the following questions:
   1. Which measure works better for the problem?
   1. What would be needed, besides good measure, to build a dictionary of multiword expressions?
   1. Can you identify a certain threshold which clearly divides the *good* expressions from the *bad*?