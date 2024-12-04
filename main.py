import os
import pandas as pd
import praw
import urllib.request
import xmltodict
import datetime
from Classes import RedditDocument, ArxivDocument

# Fonction pour collecter les données d'ArXiv
def collect_arxiv_data(query, limit=10):
    base_url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={limit}'
    response = urllib.request.urlopen(base_url).read()
    data = xmltodict.parse(response)
    docs = []
    for entry in data['feed']['entry']:
        titre = entry['title'].replace('\n', '')
        try:
            auteurs = [author['name'] for author in entry['author']]
        except TypeError:
            auteurs = [entry['author']['name']]
        texte = entry.get('summary', '').replace('\n', '')
        date = datetime.datetime.strptime(entry['published'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")
        url = entry['id']
        docs.append({
            "type": "ArXiv",
            "titre": titre,
            "auteur": auteurs[0],
            "date": date,
            "url": url,
            "texte": texte,
            "co_auteurs": ", ".join(auteurs[1:]) if len(auteurs) > 1 else ""
        })
    return docs

# Fonction pour collecter les données Reddit
def collect_reddit_data(subreddit, limit=10):
    reddit = praw.Reddit(client_id="your_client_id",
                         client_secret="your_client_secret",
                         user_agent="your_user_agent")
    hot_posts = reddit.subreddit(subreddit).hot(limit=limit)
    docs = []
    for post in hot_posts:
        if post.selftext:
            docs.append({
                "type": "Reddit",
                "titre": post.title,
                "auteur": str(post.author),
                "date": datetime.datetime.fromtimestamp(post.created).strftime("%Y/%m/%d"),
                "url": "https://www.reddit.com" + post.permalink,
                "texte": post.selftext.replace('\n', ''),
                "nb_comments": post.num_comments
            })
    return docs

# Sauvegarde des données dans un fichier CSV
def save_data_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Données sauvegardées dans {filename}")

# Chargement des données depuis un fichier CSV
def load_data_from_csv(filename):
    return pd.read_csv(filename)

# Main
if __name__ == "__main__":
    data_file = "corpus_data.csv"

    if os.path.exists(data_file):
        print("Chargement des données depuis le fichier existant...")
        data = load_data_from_csv(data_file)
    else:
        print("Aucun fichier trouvé. Collecte des données...")
        reddit_data = collect_reddit_data('travel', limit=10)
        arxiv_data = collect_arxiv_data('climate', limit=10)
        data = reddit_data + arxiv_data
        save_data_to_csv(data, data_file)

    # Affichage des données chargées
    print(f"Données chargées : {len(data)} documents")
    print(pd.DataFrame(data).head())  # Affiche les premiers documents pour vérification
