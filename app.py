from models.Corpus import Corpus

# Chargement des données
corpus = Corpus()
corpus.load_from_file('./data/data_cleaned.json')

# Affichage des statistiques du corpus
print(corpus.get_corpus_info())


texts = corpus.prepare_texts()
corpus.calculate_tf(texts)
corpus.calculate_idf(texts)
corpus.calculate_tfidf()

# Visualiser la matrice TF-IDF
tfidf_df = corpus.get_tfidf_matrix()
print(tfidf_df)