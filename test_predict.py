import unittest
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from src.predict import predict_message

class PredictTests(unittest.TestCase):
    def test_empty_text_rejected(self):
        model = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression())])
        with self.assertRaises(ValueError):
            predict_message(model, " ")

    def test_prediction_shape(self):
        texts = [
            "hello how are you",
            "meeting at the office",
            "claim your prize now",
            "urgent win a free prize",
        ]
        labels = ["ham", "ham", "spam", "spam"]
        model = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression())])
        model.fit(texts, labels)
        result = predict_message(model, "claim your prize")
        self.assertIn(result["label"], {"ham", "spam"})
        self.assertIn("estimated_probability", result)

if __name__ == "__main__":
    unittest.main()
