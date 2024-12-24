"""
Ce module contient la classe Corpus qui permet de stocker et intéragir avec les données textuelles récoltées.
"""
import pandas as pd
import json
import re
from .Classes import Author
from collections import Counter

class Corpus:
    """
    Cette classe permet de gérer et manipuler des données textuelles organisées par ville.
    """
    def __init__(self):
        self.data = {}
        self.concatenated_text = None  # Pour éviter de recalculer lors de chaque recherche

    def load_from_file(self, file_path):
        """
        Cette méthode permet de charger les données contenues dans le fichier JSON créé depuis l'api Wikivoyage.

        :param file_path: Chemin vers le fichier JSON.
        """
        
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def get_city_activities(self, city_name):
        """
        Cette méthode permet de récupérer les activités chargées pour une ville spécifique.

        :param city_name: Nom de la ville à rechercher dans les données
        """
        city_info = self.data.get(city_name, "City not found in the data.")
        activities = city_info.get("do", "City non")
        return activities
    
    def get_corpus_info(self):
        """
        Cette méthode permet d'afficher les statistiques du Corpus.
        """
        # Nombre de villes dans le corpus
        num_cities = len(self.data)
        
        # Calculer le nombre total de caractères dans la section "do" de chaque ville
        total_do_length = sum(len(details['do']) for details in self.data.values())
        
        # Calculer le nombre moyen de caractères
        avg_do_length = total_do_length / num_cities if num_cities > 0 else 0
        
        print(f"{'='*40}")
        print(f"{'Statistiques du Corpus':^40}")
        print(f"{'='*40}")
        print(f"Nombre de villes contenues dans le corpus : {num_cities}")
        print(f"Nombre moyen de caractères à traiter par ville : {avg_do_length:.0f}")

        # Compter les mots dans toutes les sections "do"
        word_counter = Counter()
        for details in self.data.values():
            # On nettoie le texte en supprimant la ponctuation et en mettant tout en minuscule
            words = re.findall(r'\b\w+\b', details['do'].lower())
            word_counter.update(words)
        
        # Obtenir les 10 mots les plus fréquents
        most_common_words = word_counter.most_common(10)
        # Affichage des 10 mots les plus fréquents
        print(f"\nLes 10 mots les plus fréquents dans le corpus :")
        for word, count in most_common_words:
            print(f"{word}: {count}")
    

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))
        return "\n".join(list(map(str, docs)))

    def search(self, keyword):
        """
        Cette méthode permet de rechercher un mot clé dans le corpus et renvoie son occurrence par ville.
        """
        # Initialiser une liste pour stocker les résultats des villes et des sections "do"
        matches = []
        
        # Recherche du mot-clé dans chaque section "do" des villes
        for city, details in self.data.items():
            # Si la ville a une section "do", on effectue la recherche
            if "do" in details:
                # Utilisation de re pour trouver les occurrences du mot-clé dans la section "do"
                pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
                city_matches = pattern.findall(details['do'])
                
                # Si le mot-clé est trouvé, on enregistre la ville et le nombre de correspondances
                if city_matches:
                    matches.append((city, len(city_matches)))
                else :
                    print("Ce mot n'est pas contenu dans ce Corpus.")
        
        return matches

    def concorde(self, keyword, window=30):
        results = []
        for doc in self.id2doc.values():
            for match in re.finditer(rf'\b{re.escape(keyword)}\b', doc.texte, re.IGNORECASE):
                start = max(match.start() - window, 0)
                end = min(match.end() + window, len(doc.texte))
                results.append({
                    "Contexte gauche": doc.texte[start:match.start()],
                    "Motif trouvé": match.group(),
                    "Contexte droit": doc.texte[match.end():end],
                })
        return pd.DataFrame(results)
