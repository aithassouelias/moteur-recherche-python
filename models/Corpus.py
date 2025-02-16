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
        self.concatenated_text = None

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
        """
        city_info = self.data.get(city_name)
        if city_info is None:
            return "City not found in the data."
        return city_info.get("do", "No activities found.")

    
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
            # Nettoyage du texte en supprimant la ponctuation et en mettant tout en minuscule
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
        # Initialisation d'une liste pour stocker les résultats des villes et des sections "do"
        matches = []
        
        # Recherche du mot-clé dans chaque section "do" des villes
        for city, details in self.data.items():
            if "do" in details:
                # Utilisation d'expression régulière pour trouver les occurrences du mot-clé dans la section "do"
                pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
                city_matches = pattern.findall(details['do'])
                
                # Mot-clé est trouvé, on enregistre la ville et le nombre de correspondances
                if city_matches:
                    matches.append((city, len(city_matches)))
                else :
                    print("Ce mot n'est pas contenu dans ce Corpus.")
        
        return matches
    
    def clean_text_to_english(self, text):
        """
        Cette méthode filtre le texte pour ne garder que les caractères anglais (lettres et ponctuation).
        
        :param text: Le texte à filtrer.
        :return: Le texte nettoyé, contenant uniquement des caractères anglais et des espaces.
        """
        # Nettoyage du texte
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?;\'"-]', '', text)
        
        # Suppression des caractères non-latin
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)

        return cleaned_text
    
    def prepare_texts(self):
        """
        Cette méthode concatène toutes les sections 'do' pour chaque ville et prépare les textes.
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
        Cette méthode calcule la matrice TF.
        """
        self.vocabulary = sorted(set(word for text in texts for word in re.findall(r'\b\w+\b', text.lower())))
        tf_matrix = []

        for text in texts:
            # Nettoyage du texte 
            text = self.clean_text_to_english(text)
            
            word_counts = Counter(re.findall(r'\b\w+\b', text.lower()))
            total_words = sum(word_counts.values())
            tf_vector = [word_counts[word] / total_words for word in self.vocabulary]
            tf_matrix.append(tf_vector)

        self.tf_matrix = np.array(tf_matrix)

    def calculate_idf(self, texts):
        """
        Cette méthode calcule le vecteur IDF.
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
        Cette méthode calcule la matrice TF-IDF à partir des matrices TF et IDF.
        """
        self.tfidf_matrix = self.tf_matrix * self.idf_vector

    def get_tfidf_matrix(self):
        """
        Cette méthode renvoie la matrice TF-IDF sous forme de DataFrame pour une visualisation.
        """
        if self.tfidf_matrix is None:
            raise ValueError("La matrice TF-IDF n'a pas encore été calculée.")
        return pd.DataFrame(
            self.tfidf_matrix,
            index=self.city_names,
            columns=self.vocabulary
        )
