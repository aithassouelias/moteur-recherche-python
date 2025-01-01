import json
import re

from nltk.corpus import stopwords
import nltk

# Télécharger les stopwords si ce n'est pas déjà fait
nltk.download('stopwords')

def clean_json(input_file, output_file):
    # Charger les données du fichier JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Liste des stop words en anglais
    stop_words = set(stopwords.words('english'))
    additional_stop_words = set([
    'around', 'many', 'thumb', 'also'
    ])
    stop_words.update(additional_stop_words)

    # Fonction pour nettoyer une chaîne de caractères
    def clean_text(text):
        # Garder uniquement les lettres françaises classiques (A-Z et a-z)
        text = re.sub(r'[^a-zA-Zéèàçêâîôûù]', ' ', text)
        # Convertir en minuscules
        text = text.lower()
        # Supprimer les stop words
        text = ' '.join(word for word in text.split() if word not in stop_words)
        # Supprimer les espaces multiples
        text = re.sub(r'\s{2,}', ' ', text)
        return text.strip()

    # Parcourir les données et nettoyer les textes
    def clean_data(data):
        if isinstance(data, dict):
            return {key: clean_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [clean_data(item) for item in data]
        elif isinstance(data, str):
            return clean_text(data)
        else:
            return data

    cleaned_data = clean_data(data)

    # Sauvegarder les données nettoyées dans un nouveau fichier JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

# Exemple d'utilisation
input_file = './data/data.json'  # Nom du fichier original
output_file = './data/data_cleaned.json'  # Nom du fichier nettoyé
clean_json(input_file, output_file)

import numpy as np

def search(mat_TFIDF, vocab):
    # Obtenir la requête utilisateur
    query = input("Entrez votre requête: ")
    
    # Diviser les mots de la requête
    query_words = query.lower().split()
    
    # Initialiser le vecteur de requête
    query_vec = np.zeros(len(vocab))
    
    # Remplir le vecteur de requête
    for word in query_words:
        if word in vocab:
            query_vec[vocab[word]['unique_id']] = 1
    
    # Calculer la similarité cosinus entre la requête et les documents
    query_norm = np.linalg.norm(query_vec)
    if query_norm == 0:
        print("Aucun mot de la requête n'est dans le vocabulaire.")
        return -1
    
    doc_norms = np.linalg.norm(mat_TFIDF.todense(), axis=1)
    cos_sim = np.zeros(len(doc_norms))
    
    for i, doc_norm in enumerate(doc_norms):
        if doc_norm != 0:
            cos_sim[i] = np.array(mat_TFIDF.todense()[i, :]).flatten().dot(query_vec) / (doc_norm * query_norm)
    
    # Sortir le document le plus similaire
    most_similar_doc = np.argmax(cos_sim)
    return cos_sim, most_similar_doc
