"""
Ce module contient la classe Corpus qui permet de stocker et intéragir avec les données textuelles récoltées.
"""
import math
import pandas as pd
import json
import re
import numpy as np
from collections import Counter, defaultdict

class Corpus:
    """
    Cette classe permet de gérer et manipuler des données textuelles organisées par ville.
    """
    def __init__(self):
        self.data = {}
        self.cleaned_data = {}
        self.concatenated_text = None  # Pour éviter de recalculer lors de chaque recherche

    def load_from_files(self, data_file_path, cleaned_file_path):
        """
        Charge les données à partir de deux fichiers : un fichier complet et un fichier nettoyé.
        """
        # Charger le fichier data.json (données complètes)
        with open(data_file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        
        # Charger le fichier data_cleaned.json (données nettoyées)
        with open(cleaned_file_path, 'r', encoding='utf-8') as file:
            self.cleaned_data = json.load(file)

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
    
    def clean_text_to_english(self, text):
        """
        Filtre le texte pour ne garder que les caractères anglais (lettres et ponctuation).
        
        :param text: Le texte à filtrer.
        :return: Le texte nettoyé, contenant uniquement des caractères anglais et des espaces.
        """
        # Filtrer le texte pour ne conserver que les caractères de l'alphabet anglais et les espaces.
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?;\'"-]', '', text)
        
        # Supprimer les caractères non-latin (par exemple, le cyrillique, les caractères asiatiques)
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)

        return cleaned_text
    
    def prepare_texts(self):
        """
        Concatène toutes les sections 'do' pour chaque ville et prépare les textes.
        """
        texts = []
        self.city_names = []
        for city, details in self.data.items():
            if "do" in details:
                texts.append(details["do"])
                self.city_names.append(city)
        return texts

    def calculate_tf(self, texts):
        """
        Calcule la matrice TF (Term Frequency).
        """
        self.vocabulary = sorted(set(word for text in texts for word in re.findall(r'\b\w+\b', text.lower())))
        tf_matrix = []

        for text in texts:
            # Nettoyer le texte pour ne conserver que l'anglais
            text = self.clean_text_to_english(text)
            
            word_counts = Counter(re.findall(r'\b\w+\b', text.lower()))
            total_words = sum(word_counts.values())
            tf_vector = [word_counts[word] / total_words for word in self.vocabulary]
            tf_matrix.append(tf_vector)

        self.tf_matrix = np.array(tf_matrix)

    def calculate_idf(self, texts):
        """
        Calcule le vecteur IDF (Inverse Document Frequency).
        """
        num_documents = len(texts)
        doc_frequency = defaultdict(int)

        for word in self.vocabulary:
            for text in texts:
                if word in text.lower():
                    doc_frequency[word] += 1

        self.idf_vector = np.array([
            math.log((num_documents / (doc_frequency[word] + 1))) for word in self.vocabulary
        ])

    def calculate_tfidf(self):
        """
        Calcule la matrice TF-IDF à partir des matrices TF et IDF.
        """
        self.tfidf_matrix = self.tf_matrix * self.idf_vector

    def get_tfidf_matrix(self):
        """
        Renvoie la matrice TF-IDF sous forme de DataFrame pour une visualisation.
        """
        if self.tfidf_matrix is None:
            raise ValueError("La matrice TF-IDF n'a pas encore été calculée.")
        return pd.DataFrame(
            self.tfidf_matrix,
            index=self.city_names,
            columns=self.vocabulary
        )

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
