import unittest
from unittest.mock import patch, mock_open
from Corpus import Corpus
import numpy as np

class TestCorpus(unittest.TestCase):

    def setUp(self):
        """Initialisation de la classe Corpus pour les tests."""
        self.corpus = Corpus()
        self.sample_data = {
            "Paris": {"do": "Visit the Eiffel Tower and enjoy the Seine."},
            "London": {"do": "Explore the British Museum and the Tower of London."},
        }
        self.sample_cleaned_data = {
            "Paris": {"do": "Eiffel Tower Seine."},
            "London": {"do": "British Museum Tower."},
        }

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_load_from_files(self, mock_json_load, mock_file):
        """Test pour la méthode load_from_files."""
        mock_json_load.side_effect = [self.sample_data, self.sample_cleaned_data]
        self.corpus.load_from_files("data.json", "data_cleaned.json")
        self.assertEqual(self.corpus.data, self.sample_data)
        self.assertEqual(self.corpus.cleaned_data, self.sample_cleaned_data)

    def test_get_city_activities(self):
        """Test pour la méthode get_city_activities."""
        self.corpus.data = self.sample_data
        activities = self.corpus.get_city_activities("Paris")
        self.assertEqual(activities, "Visit the Eiffel Tower and enjoy the Seine.")

        activities_not_found = self.corpus.get_city_activities("Berlin")
        self.assertEqual(activities_not_found, "City not found in the data.")

    def test_clean_text_to_english(self):
        """Test pour la méthode clean_text_to_english."""
        text = "Visitez la Tour Eiffel ! C'est magnifique \u2764"
        cleaned_text = self.corpus.clean_text_to_english(text)
        self.assertEqual(cleaned_text, "Visitez la Tour Eiffel ! C'est magnifique")

    def test_calculate_tf(self):
        """Test pour la méthode calculate_tf."""
        texts = ["Visit the Eiffel Tower.", "Enjoy the Tower."]
        self.corpus.calculate_tf(texts)
        expected_vocab = sorted(["enjoy", "eiffel", "the", "tower", "visit"])
        self.assertEqual(self.corpus.vocabulary, expected_vocab)
        self.assertTrue(isinstance(self.corpus.tf_matrix, np.ndarray))

    def test_calculate_idf(self):
        """Test pour la méthode calculate_idf."""
        texts = ["Visit the Eiffel Tower.", "Enjoy the Tower."]
        self.corpus.calculate_tf(texts)
        self.corpus.calculate_idf(texts)
        self.assertTrue(isinstance(self.corpus.idf_vector, np.ndarray))

    def test_calculate_tfidf(self):
        """Test pour la méthode calculate_tfidf."""
        texts = ["Visit the Eiffel Tower.", "Enjoy the Tower."]
        self.corpus.calculate_tf(texts)
        self.corpus.calculate_idf(texts)
        self.corpus.calculate_tfidf()
        self.assertTrue(isinstance(self.corpus.tfidf_matrix, np.ndarray))

    def test_get_tfidf_matrix(self):
        """Test pour la méthode get_tfidf_matrix."""
        texts = ["Visit the Eiffel Tower.", "Enjoy the Tower."]
        self.corpus.calculate_tf(texts)
        self.corpus.calculate_idf(texts)
        self.corpus.calculate_tfidf()
        tfidf_df = self.corpus.get_tfidf_matrix()
        self.assertTrue(isinstance(tfidf_df, pd.DataFrame))
        self.assertEqual(list(tfidf_df.index), [])

if __name__ == "__main__":
    unittest.main()
