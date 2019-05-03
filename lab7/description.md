## Tasks

1. Read the documentation of [word2vec](https://radimrehurek.com/gensim/models/word2vec.html) in Gensim library.
1. Download polish word embeddings for word2vec from [Clarin](https://clarin-pl.eu/dspace/handle/11321/327).
1. Using the downloaded model find the most similar word or expressions for the following expressions:
   1. sąd wysoki
   1. trybunał konstytucyjny
   1. kodeks cywilny
   1. kpk
   1. sąd rejonowy
   1. szkoda
   1. wypadek
   1. kolizja
   1. szkoda majątkowy
   1. nieszczęście
   1. rozwód
1. Find the result of the following equations (5 top results):
   1. sąd wysoki - kpc + konstytucja
   1. pasażer - mężczyzna + kobieta
   1. samochód - droga + rzeka
1. Using the [t-SNE](http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) 
   algorithm comput the projection of the random 1000 words with the following words highlighted
   (assuming they are available):
   1. szkoda
   1. strata
   1. uszczerbek
   1. szkoda majątkowy
   1. uszczerbek na zdrowie
   1. krzywda
   1. niesprawiedliwość
   1. nieszczęście