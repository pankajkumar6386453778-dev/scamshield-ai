"""Train a text classifier from the UCI SMS Spam Collection file.

Expected input:
  data/SMSSpamCollection
  Tab-separated rows: label<TAB>message

Download the dataset from:
https://archive.ics.uci.edu/dataset/228/sms+spam+collection
Extract the file into the data/ directory before running this script.
"""
from pathlib import Path
import json
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "SMSSpamCollection"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Download/extract the UCI SMS Spam Collection first; see README.md."
        )

    df = pd.read_csv(DATA_PATH, sep="\t", header=None, names=["label", "message"], encoding="utf-8")
    df = df.dropna(subset=["label", "message"])
    df["label"] = df["label"].astype(str).str.lower().str.strip()
    df["message"] = df["message"].astype(str).str.strip()
    df = df[df["label"].isin(["ham", "spam"])]
    df = df.drop_duplicates(subset=["label", "message"]).reset_index(drop=True)

    if df.empty or df["label"].nunique() != 2:
        raise ValueError("Dataset must contain both ham and spam labels.")

    X_train, X_test, y_train, y_test = train_test_split(
        df["message"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    candidates = {
        "logistic_regression": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=20000, sublinear_tf=True)),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
        ]),
        "multinomial_nb": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=20000, sublinear_tf=True)),
            ("classifier", MultinomialNB()),
        ]),
    }

    results = {}
    fitted = {}
    for name, candidate in candidates.items():
        candidate.fit(X_train, y_train)
        pred = candidate.predict(X_test)
        results[name] = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "spam_precision": float(precision_score(y_test, pred, pos_label="spam", zero_division=0)),
            "spam_recall": float(recall_score(y_test, pred, pos_label="spam", zero_division=0)),
            "spam_f1": float(f1_score(y_test, pred, pos_label="spam", zero_division=0)),
        }
        fitted[name] = candidate
        print(f"\\n{name}")
        print(classification_report(y_test, pred, labels=["ham", "spam"], zero_division=0))
        print("Confusion matrix [ham, spam]:")
        print(confusion_matrix(y_test, pred, labels=["ham", "spam"]))

    # Select by spam F1, then spam recall as a tie-breaker.
    best_name = max(results, key=lambda n: (results[n]["spam_f1"], results[n]["spam_recall"]))
    best_model = fitted[best_name]
    best_pred = best_model.predict(X_test)
    best_metrics = dict(results[best_name])
    best_metrics["selected_model"] = best_name
    best_metrics["dataset_rows_after_cleaning"] = int(len(df))
    best_metrics["train_rows"] = int(len(X_train))
    best_metrics["test_rows"] = int(len(X_test))
    best_metrics["confusion_matrix"] = confusion_matrix(
        y_test, best_pred, labels=["ham", "spam"]
    ).tolist()
    best_metrics["label_order"] = ["ham", "spam"]
    best_metrics["candidate_results"] = results

    joblib.dump(best_model, MODEL_DIR / "message_model.joblib")
    (MODEL_DIR / "metrics.json").write_text(json.dumps(best_metrics, indent=2), encoding="utf-8")
    print(f"\\nSelected model: {best_name}")
    print(json.dumps(best_metrics, indent=2))
    print(f"Saved model to {MODEL_DIR / 'message_model.joblib'}")

if __name__ == "__main__":
    main()
