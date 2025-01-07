from models.Corpus import Corpus
from models.SearchEngine import SearchEngine
from models.SearchInterface import SearchInterface
import tkinter as tk

# Chargement des données
corpus = Corpus()
corpus.load_from_files('./data/data.json', './data/data_cleaned.json')

# Initialisation du moteur de recherche
search_engine = SearchEngine(corpus)

# Lancement de l'interface
def main():
    root = tk.Tk()
    app = SearchInterface(root, search_engine)
    root.mainloop()

if __name__ == "__main__":
    main()