class Document:
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}"

    def __str__(self):
        return f"{self.titre}, par {self.auteur}"


class RedditDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", nb_comments=0):
        super().__init__(titre, auteur, date, url, texte)
        self.nb_comments = nb_comments

    def __repr__(self):
        return super().__repr__() + f"\t# Comments : {self.nb_comments}"

    def __str__(self):
        return f"{self.titre}, par {self.auteur} ({self.nb_comments} commentaires)"


class ArxivDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", co_auteurs=None):
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs or []

    def __repr__(self):
        co_auteurs_str = ", ".join(self.co_auteurs)
        return super().__repr__() + f"\tCo-auteurs : {co_auteurs_str}"

    def __str__(self):
        return f"{self.titre}, par {self.auteur} et co-auteurs ({', '.join(self.co_auteurs)})"


class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []

    def add(self, production):
        self.ndoc += 1
        self.production.append(production)

    def __str__(self):
        return f"Auteur : {self.name}\t# Productions : {self.ndoc}"
