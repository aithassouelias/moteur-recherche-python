from models.Corpus import Corpus
from models.SearchEngine import SearchEngine

# Chargement des données
corpus = Corpus()
corpus.load_from_files('./data/data.json','./data/data_cleaned.json')

search_engine = SearchEngine(corpus)

query = "watch football game"
results = search_engine.search(query, top_n=10)
print(results)
