from models.Corpus import Corpus

corpus = Corpus()
corpus.load_from_file('./data/data.json')


print(corpus.get_corpus_info())

keyword = "walk"
matches = corpus.search(keyword)

# Affichage des résultats
for city, count in matches:
    print(f"Ville: {city}, Nombre d'occurrences du mot {keyword} : {count}")

corpus.display_tfidf_matrix()