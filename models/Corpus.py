from Classes import Author, RedditDocument, ArxivDocument
import pandas as pd
import re

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.concatenated_text = None  # Pour éviter de recalculer lors de chaque recherche

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
        if not self.concatenated_text:
            self.concatenated_text = " ".join(doc.texte for doc in self.id2doc.values())
        pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
        matches = pattern.findall(self.concatenated_text)
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

    def stats(self, top_n=10):
        vocab = {}
        for doc in self.id2doc.values():
            for word in re.findall(r'\w+', doc.texte.lower()):
                vocab[word] = vocab.get(word, 0) + 1
        sorted_vocab = sorted(vocab.items(), key=lambda x: x[1], reverse=True)
        print(f"Nombre total de mots : {len(vocab)}")
        print(f"Top {top_n} mots fréquents : {sorted_vocab[:top_n]}")
