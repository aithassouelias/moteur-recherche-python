"""
Ce module contient la classe SearchInterface qui permet créer l'interface graphique Tkinter et effectuer une recherche.
"""
import tkinter as tk

class SearchInterface:
    """
    Cette classe inclut 2 méthodes permettant de créer l'interface graphique Tkinter et permettre à l'utilisateur de réaliser une recherche.
    """
    def __init__(self, root, search_engine):
        """
        Cette méthode permet de créer l'interface graphique Tkinter
        """
        self.root = root
        self.search_engine = search_engine

        # Configuration de la fenêtre principale
        self.root.title("Moteur de recherche des villes")
        self.root.geometry("600x700")

        # Barre de recherche
        self.search_label = tk.Label(root, text="Recherchez une ville, un mot-clé ou une phrase :")
        self.search_label.pack(pady=10)

        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.pack(pady=5)

        # Nombre maximum de résultats
        self.max_results_label = tk.Label(root, text="Nombre maximum de résultats à afficher :")
        self.max_results_label.pack(pady=10)

        self.max_results_entry = tk.Entry(root, width=10)
        self.max_results_entry.insert(0, "10")  # Valeur par défaut
        self.max_results_entry.pack(pady=5)

        # Boutons
        self.search_button = tk.Button(root, text="Rechercher", command=self.perform_search)
        self.search_button.pack(pady=10)

        # Zone de résultats
        self.result_label = tk.Label(root, text="Résultats :")
        self.result_label.pack(pady=10)

        self.result_box = tk.Text(root, height=25, width=70, wrap="word", state="disabled")
        self.result_box.pack(pady=5)

    def perform_search(self):
        """
        Cette méthode permet de réaliser une recherche en appelant la méthode search de la classe SearchEngine
        """
        # Récupération de la requête utilisateur
        query = self.search_entry.get()

        # Récupération du nombre maximum de résultats
        try:
            max_results = int(self.max_results_entry.get())
        except ValueError:
            max_results = 10  # Par défaut si l'utilisateur entre une valeur non valide

        # Recherche avec le moteur de recherche
        results_df = self.search_engine.search(query, top_n=max_results)

        # Affichage des résultats
        self.result_box.config(state="normal")
        self.result_box.delete(1.0, tk.END)  # Effacer les anciens résultats

        if not results_df.empty:
            for _, row in results_df.iterrows():
                city_name = row['City']
                similarity_score = row['Similarity Score']
                city_info = self.search_engine.corpus.get_city_activities(city_name)
                self.result_box.insert(tk.END, f"Ville : {city_name}\nScore de similarité : {similarity_score:.4f}\nDonnées associées : {city_info}\n{'-'*40}\n")
        else:
            self.result_box.insert(tk.END, "Aucun résultat trouvé.")

        self.result_box.config(state="disabled")
