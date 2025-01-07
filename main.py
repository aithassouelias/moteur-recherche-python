from models.Corpus import Corpus
import tkinter as tk

# Chargement des données
corpus = Corpus()
corpus.load_from_files('./data/data.json','./data/data_cleaned.json')

# Fonctionnalités de l'interface
class SearchInterface:
    def __init__(self, root, corpus):
        self.root = root
        self.corpus = corpus

        # Configuration de la fenêtre principale
        self.root.title("Moteur de recherche des villes")
        self.root.geometry("600x600")

        # Barre de recherche
        self.search_label = tk.Label(root, text="Recherchez une ville, un mot-clé ou une phrase :")
        self.search_label.pack(pady=10)

        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.pack(pady=5)

        # Boutons
        self.search_button = tk.Button(root, text="Rechercher", command=self.perform_search)
        self.search_button.pack(pady=10)

        self.stats_button = tk.Button(root, text="Afficher les statistiques", command=self.display_corpus_stats)
        self.stats_button.pack(pady=5)

        # Zone de résultats
        self.result_label = tk.Label(root, text="Résultats :")
        self.result_label.pack(pady=10)

        self.result_box = tk.Text(root, height=25, width=70, wrap="word", state="disabled")
        self.result_box.pack(pady=5)

    def perform_search(self):
        # Récupération de la requête utilisateur
        query = self.search_entry.get()

        # Recherche dans le corpus
        results = self.corpus.search(query)

        # Affichage des résultats
        self.result_box.config(state="normal")
        self.result_box.delete(1.0, tk.END)  # Effacer les anciens résultats

        if results:
            for city, count in results:
                city_info = self.corpus.get_city_activities(city)
                self.result_box.insert(tk.END, f"Ville : {city}\nOccurences : {count}\nActivités : {city_info}\n{'-'*40}\n")
        else:
            self.result_box.insert(tk.END, "Aucun résultat trouvé.")

        self.result_box.config(state="disabled")

    def display_corpus_stats(self):
        # Afficher les statistiques du corpus dans la zone de résultats
        self.result_box.config(state="normal")
        self.result_box.delete(1.0, tk.END)

        try:
            # Capture les informations affichées par get_corpus_info
            stats_info = []

            def capture_print(*args):
                stats_info.append(" ".join(map(str, args)))

            # Redirige le print temporairement
            import builtins
            original_print = builtins.print
            builtins.print = capture_print

            self.corpus.get_corpus_info()

            # Rétablit le print
            builtins.print = original_print

            # Affiche les statistiques dans la zone de texte
            self.result_box.insert(tk.END, "\n".join(stats_info))

        except Exception as e:
            self.result_box.insert(tk.END, f"Erreur lors de l'affichage des statistiques : {e}")

        self.result_box.config(state="disabled")

# Lancement de l'interface
def main():
    root = tk.Tk()
    app = SearchInterface(root, corpus)
    root.mainloop()

if __name__ == "__main__":
    main()
