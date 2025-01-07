# Moteur de recherche touristique en Python

## Présentation du projet

Ce projet a pour objectif de développer un moteur de recherche textuel sur des données touristiques issues de l'API WikiVoyage en utilisant le langage de programmation Python. Le moteur de recherche permet aux utilisateurs de rechercher des activités qu'ils souhaitent réaliser et retourne des descriptions de villes où ces activités sont disponibles. 

## Fonctionnalités
- Recherche d'activités touristiques par mots-clés.
- Extraction des descriptions touristiques à partir de l’API WikiVoyage.
- Affichage des villes proposant l'activité recherchée.

## Prérequis
- Python 3.8 ou version supérieure
- Bibliothèques Python : `requests`, `json`, `pandas`
- Accès à l'API WikiVoyage

## Installation
1. Clonez le dépôt :  
   ```bash
   git clone https://github.com/votre-utilisateur/moteur-recherche-touristique.git

2. Installez les dépendances :  
pip install -r requirements.txt

3. Lancez le projet :  
python main.py

## Utilisation
1. Entrez un mot-clé correspondant à une activité touristique (par ex. "randonnée").  
2. Le moteur de recherche affichera une liste de villes et leurs descriptions.  
3. Exemple :  
   ```bash
   > Activité recherchée : randonnée  
   > Résultats :  
      - Marrakech : "Découvrez les montagnes de l'Atlas..."  
      - Barcelone : "Partez en randonnée dans le parc de Collserola..."

## Architecture du projet
- `main.py` : Point d’entrée du programme.
- `data/` : Contient les données brutes collectées.
- `models/` : Classes Python pour gérer les données.
- `utils.py` : Fonctions utilitaires pour le traitement des données.

## Contributions
Les contributions sont les bienvenues !  
1. Forkez le dépôt.  
2. Créez une branche pour vos modifications :  
   ```bash
   git checkout -b feature/ma-fonctionnalite


## Auteurs
Développé par : 
- [Timothy Marcia](https://github.com/TimothyMarcia)
- [Elias Ait Hassou](https://github.com/aithassouelias)

