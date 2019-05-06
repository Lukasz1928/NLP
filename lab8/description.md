## Tasks

1. Divide the set of bills into two exclusive sets:
   1. the set of bills amending other bills (their title starts with `o zmianie ustawy`),
   1. the set of bills not amending other bills.
1. Change the contents of the bill by removing the date of publication and the title (so the words `o zmianie ustawy`
   are removed).
1. Split the sets of documents into the following groups by randomly selecting the documents:
   1. 60% training
   1. 20% validation
   1. 20% testing
1. Do not change these groups during the following experiments.
1. Prepare the following variants of the documents:
   1. full text of the document
   1. randomly selected 10% of the lines of the document
   1. randomly selected 10 lines of the document
   1. randomly selected 1 line of the document
1. Train the following classifiers on the documents:
   1. SVM with TF•IDF
   1. Fasttext
   1. Flair with Polish language model
1. Report Precision, Recall and F1 for each variant of the experiment (12 variants altogether).