"""
Ce module contient la classe SearchEngine qui permet de réaliser la recherche par mots-clés.
"""
import numpy as np
import pandas as pd
from collections import Counter
import re

class SearchEngine:
    def __init__(self, corpus):
        """
        Initialisation du moteur de recherche avec un objet Corpus.
        Lors de l'initialisation, nous calculons la matrice TF-IDF.
        """
        self.corpus = corpus
        # Charger et préparer les textes
        self.texts = corpus.prepare_texts()
        # Calculer TF et IDF
        self.corpus.calculate_tf(self.texts)
        self.corpus.calculate_idf(self.texts)
        # Calculer la matrice TF-IDF
        self.corpus.calculate_tfidf()

    def transform_query_to_vector(self, query):
        """
        Transforme une requête sous forme de texte en un vecteur de termes
        en fonction du vocabulaire du corpus.
        """
        # Nettoyer et séparer les mots de la requête
        query_words = re.findall(r'\b\w+\b', query.lower())
        query_word_counts = Counter(query_words)
        
        # Vecteur pour la requête
        query_vector = np.zeros(len(self.corpus.vocabulary))

        # Remplir le vecteur de la requête avec les occurrences des mots de la requête
        for i, word in enumerate(self.corpus.vocabulary):
            query_vector[i] = query_word_counts.get(word, 0)

        return query_vector

    def calculate_cosine_similarity(self, query_vector, doc_vector):
        """
        Calcule la similarité cosinus entre la requête et un vecteur de document.
        """
        dot_product = np.dot(query_vector, doc_vector)
        norm_query = np.linalg.norm(query_vector)
        norm_doc = np.linalg.norm(doc_vector)
        
        # Eviter la division par zéro
        if norm_query == 0 or norm_doc == 0:
            return 0
        return dot_product / (norm_query * norm_doc)

    def search(self, query, top_n=5):
        """
        Recherche les documents les plus pertinents en fonction de la requête.
        
        :param query: La requête sous forme de texte.
        :param top_n: Le nombre de résultats à retourner (par défaut 5).
        
        :return: Un DataFrame contenant les résultats triés par similarité.
        """
        # Transformer la requête en vecteur
        query_vector = self.transform_query_to_vector(query)

        # Initialiser une liste pour les résultats
        similarities = []

        # Calculer la similarité entre la requête et chaque document
        for i, doc_vector in enumerate(self.corpus.tfidf_matrix):
            similarity_score = self.calculate_cosine_similarity(query_vector, doc_vector)
            similarities.append((self.corpus.city_names[i], similarity_score))

        # Trier les résultats par score de similarité (du plus élevé au plus faible)
        sorted_results = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Sélectionner les meilleurs résultats
        top_results = sorted_results[:top_n]

        # Créer un DataFrame avec les résultats
        results_df = pd.DataFrame(top_results, columns=["City", "Similarity Score"])

        return results_df
