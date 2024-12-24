"""
Ce module regroupe les différentes fonctions permettant de récupérer les données depuis l'API Wikivoyage et les stocker dans un fichier JSON.
"""
import requests
import mwparserfromhell
import json
import os

# Fonction pour récupérer l'index des sections et les afficher
def get_section_indices(city_name:str, section_name:str)->str:
    """
    Cette fonction permet de récupérer l'index de la section que l'on souhaite récupérer sur la page Wikivoyage

    :param city_name: Nom de la ville recherchée.
    :param section_name: Nom de la section recherchée.

    :return: Retourne l'index de la section recherchée.
    """
    API_URL = "https://en.wikivoyage.org/w/api.php"
    params_sections = {
        "action": "parse",
        "page": city_name,
        "format": "json",
        "prop": "sections",  # Récupère la liste des sections
    }
    
    response_sections = requests.get(API_URL, params=params_sections)
    
    if response_sections.status_code == 200:
        data_sections = response_sections.json()
        if "parse" in data_sections:
            for section in data_sections["parse"]["sections"]:
                if section["line"].lower() == section_name:
                    return section["index"]
        else:
            print(f"Page introuvable pour la ville : {city_name}")
            return None
    else:
        print(f"Erreur : {response_sections.status_code}")
        return None

# Fonction pour récupérer le contenu d'une section
def get_section_content(city_name:str, section_index:int)-> str:
    """
    Cette fonction permet de récupérer les données textuelles depuis l'API wikivoyage pour une ville et section spécifique

    :param city_name: Nom de la ville à rechercher.
    :param section_index: Index de la section à récupérer.

    :return: Retourne le contenu de la section recherchée.
    """
    API_URL = "https://en.wikivoyage.org/w/api.php"
    params_content = {
        "action": "parse",
        "page": city_name,
        "format": "json",
        "prop": "wikitext",
        "section": section_index,
    }
    
    response_content = requests.get(API_URL, params=params_content)
    
    if response_content.status_code == 200:
        data_content = response_content.json()
        if "parse" in data_content:
            wikitext = data_content["parse"]["wikitext"]["*"]
            # Convertir en texte lisible
            wiki_code = mwparserfromhell.parse(wikitext)
            plain_text = wiki_code.strip_code()
            return plain_text
        else:
            return None
    else:
        print(f"Erreur : {response_content.status_code}")
        return None

# Fonction pour sauvegarder les données dans data.json
def save_to_json(city_name:str, section_content:str):
    """
    Cette fonction permet d'enregistrer les données récoltées pour une ville spécifique dans un fichier JSON.

    :param city_name: Nom de la ville à rechercher.
    :param section_content: Section à enregistrer.
    """
    file_name = "data.json"
    
    # Charger les données existantes si le fichier existe
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    else:
        data = {}
    
    # Ajouter ou mettre à jour les données de la ville
    data[city_name] = {"do": section_content}
    
    # Sauvegarder les données dans le fichier
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Données de {city_name} sauvegardées.")

# Script principal pour parcourir une liste de villes
def main():
    """
    Cette fonction permet de créer le fichier json final à partir d'une liste de villes et de la section que l'on souhaite récupérer.
    """
    # Liste des villes
    cities = [
        "Tokyo", "New York", "Paris", "London", "Shanghai", "Dubai", "Mumbai", "Istanbul", "Beijing", "Los Angeles",
        "Mexico City", "Seoul", "Bangkok", "Moscow", "São Paulo", "Delhi", "Jakarta", "Cairo", "Buenos Aires", "Rio de Janeiro",
        "Lagos", "Karachi", "Tehran", "Johannesburg", "Hong Kong", "Sydney", "Berlin", "Madrid", "Rome", "Kuala Lumpur",
        "Singapore", "Bogotá", "Lima", "Toronto", "Chicago", "San Francisco", "Bangkok", "Chennai", "Melbourne", "Riyadh",
        "Cape Town", "Athens", "Barcelona", "Manila", "Abu Dhabi", "Santiago", "Brussels", "Stockholm", "Warsaw", "Vienna",
        "Hanoi", "Munich", "Copenhagen", "Dublin", "Zürich", "Oslo", "Lisbon", "Prague", "Helsinki", "Brisbane",
        "Auckland", "Edinburgh", "Glasgow", "Milan", "Naples", "Valencia", "Bucharest", "Budapest", "Warsaw", "Sofia",
        "Belgrade", "Vilnius", "Tallinn", "Riga", "Ljubljana", "Sarajevo", "Skopje", "Tirana", "Podgorica", "Reykjavik",
        "Doha", "Casablanca", "Marrakech", "Fes", "Tangier", "Ouarzazate", "Rabat", "Addis Ababa", "Nairobi", "Dar es Salaam",
        "Accra", "Algiers", "Tunis", "Tripoli", "Bamako", "Dakar", "Niamey", "Lusaka",
    ]
    
    # Section d'intérêt
    section_to_find = "do"
    
    for city_name in cities:
        print(f"\nTraitement de la ville : {city_name}")
        # Récupération de l'index de la section "Do"
        section_index = get_section_indices(city_name, section_to_find)
        
        if section_index:
            print(f"Section '{section_to_find.capitalize()}' trouvée pour {city_name}.")
            
            # Récupérer le contenu de la section
            section_content = get_section_content(city_name, section_index)
            if section_content:
                # Sauvegarder dans le fichier JSON
                save_to_json(city_name, section_content)
            else:
                print(f"Aucun contenu trouvé pour la section '{section_to_find.capitalize()}' de {city_name}.")
        else:
            print(f"Section '{section_to_find.capitalize()}' introuvable pour la ville : {city_name}.")

# Exécution du script
if __name__ == "__main__":
    main()
