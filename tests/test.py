import pytest
from io import StringIO
import sys
import os

@pytest.fixture
def corpus():
    sys.path.append(os.path.abspath(".."))
    from models.Corpus import Corpus
    corpus = Corpus()
    corpus.data = {
        "Paris": {"do": "Visit the Eiffel Tower and enjoy the Seine cruise."},
        "London": {"do": "Explore the British Museum and Buckingham Palace."},
        "New York": {"do": "Walk in Central Park and visit Times Square."}
    }
    return corpus

def test_get_corpus_info(corpus):
    captured_output = StringIO()
    sys.stdout = captured_output

    # Appeler la méthode
    corpus.get_corpus_info()

    # Restaurer la sortie standard
    sys.stdout = sys.__stdout__

    # Vérifier la sortie
    output = captured_output.getvalue()
    expected_output = (
        "=" * 40 + "\n"
        + f"{'Statistiques du Corpus':^40}\n"
        + "=" * 40 + "\n"
        + f"Nombre de villes contenues dans le corpus : 3\n"
        + f"Nombre moyen de caractères à traiter par ville : 46\n"
    )
    assert output == expected_output

