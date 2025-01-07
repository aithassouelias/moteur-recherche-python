"""
Ce module regroupe les différentes fonctions permettant de nettoyer le corpus.
"""
import json
import re
import numpy as np
from nltk.corpus import stopwords
import nltk

# Téléchargement des stopwords
nltk.download('stopwords')


def clean_text(text, stop_words):
    """
    Cette fonction permet de nettoyer un texte

    :param text: Le texte à nettoyer
    :param stop_words: Liste des stop_words
    """
    # Garder uniquement l'alphabet latin
    text = re.sub(r'[^a-zA-Z]', ' ', text)

    # Conversion en minuscules
    text = text.lower()

    # Suppression des stop words
    text = ' '.join(word for word in text.split() if word not in stop_words)
    # Suppression des espaces multiples
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def clean_data(data, stop_words):
    if isinstance(data, dict):
        return {key: clean_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    elif isinstance(data, str):
        return clean_text(data, stop_words)
    else:
        return data

def clean_json(input_file, output_file):
    """
    Cette fonction permet de nettoyer les données du fichier JSON initial et les stocker dans un nouveau fichier JSON

    :param input_file: Fichier JSON avec les données brutes
    :param output_file: Fichier JSON dans lequel seront stockées les données nettoyées
    """
    # Lecture des données données du fichier JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Liste des stop words en anglais
    stop_words = set(stopwords.words('english'))
    additional_stop_words = set([
    'around', 'many', 'thumb', 'also'
    ])
    stop_words.update(additional_stop_words)

    # Nettoyage des données
    cleaned_data = clean_data(data, stop_words)

    # Sauvegarde des données nettoyées dans un nouveau fichier JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

def main_clean_json() :
    """
    Fonction principale pour nettoyer et stocker les données nettoyées
    """
    input_file = './data/data.json'  
    output_file = './data/data_cleaned.json'  
    clean_json(input_file, output_file)