"""
Basic ML classifier for the Bug Tracking System.
Uses a Naive Bayes text classifier (scikit-learn) to predict a bug's
category and severity from its description. Trained on a small
labeled sample set — simple by design.
"""

import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

MODEL_DIR = "models"
CATEGORY_MODEL_PATH = f"{MODEL_DIR}/category_model.pkl"
SEVERITY_MODEL_PATH = f"{MODEL_DIR}/severity_model.pkl"

# Small labeled training set — simple hand-crafted examples covering
# common bug types. Basic by design, easy to extend.
TRAINING_DATA = [
    ("App crashes when clicking submit button", "UI", "High"),
    ("Button color does not match design spec", "UI", "Low"),
    ("Dropdown menu overlaps with header on mobile", "UI", "Medium"),
    ("Login page layout breaks on small screens", "UI", "Medium"),
    ("Text field placeholder text is misspelled", "UI", "Low"),

    ("Server returns 500 error on user registration", "Backend", "High"),
    ("API response time is slow under normal load", "Backend", "Medium"),
    ("Null pointer exception in payment processing service", "Backend", "High"),
    ("Background job fails silently without logging error", "Backend", "Medium"),
    ("Incorrect status code returned for valid request", "Backend", "Low"),

    ("Database connection times out during peak hours", "Database", "High"),
    ("Duplicate records being inserted into orders table", "Database", "High"),
    ("Query missing index causing slow report generation", "Database", "Medium"),
    ("Foreign key constraint violation on delete", "Database", "Medium"),
    ("Migration script leaves orphaned rows in table", "Database", "Low"),

    ("Application freezes when loading large dataset", "Performance", "High"),
    ("Page load time increased after latest deployment", "Performance", "Medium"),
    ("Memory usage grows continuously causing crash", "Performance", "High"),
    ("Image gallery takes too long to render", "Performance", "Low"),
    ("CPU spikes to 100 percent during file export", "Performance", "Medium"),

    ("User able to access admin panel without authentication", "Security", "High"),
    ("SQL injection possible in search input field", "Security", "High"),
    ("Password stored in plain text in database", "Security", "High"),
    ("Session token does not expire after logout", "Security", "Medium"),
    ("CSRF protection missing on settings form", "Security", "Medium"),
]


def train_classifiers():
    descriptions = [d[0] for d in TRAINING_DATA]
    categories = [d[1] for d in TRAINING_DATA]
    severities = [d[2] for d in TRAINING_DATA]

    category_model = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        ("clf", MultinomialNB()),
    ])
    category_model.fit(descriptions, categories)

    severity_model = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        ("clf", MultinomialNB()),
    ])
    severity_model.fit(descriptions, severities)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(category_model, CATEGORY_MODEL_PATH)
    joblib.dump(severity_model, SEVERITY_MODEL_PATH)
    print(f"Trained and saved category + severity classifiers to {MODEL_DIR}/")


def load_classifiers():
    if not (os.path.exists(CATEGORY_MODEL_PATH) and os.path.exists(SEVERITY_MODEL_PATH)):
        train_classifiers()
    category_model = joblib.load(CATEGORY_MODEL_PATH)
    severity_model = joblib.load(SEVERITY_MODEL_PATH)
    return category_model, severity_model


def classify_bug(description, category_model=None, severity_model=None):
    if category_model is None or severity_model is None:
        category_model, severity_model = load_classifiers()
    category = category_model.predict([description])[0]
    severity = severity_model.predict([description])[0]
    return category, severity


if __name__ == "__main__":
    train_classifiers()

    # quick sanity check
    test_bugs = [
        "Page crashes when uploading a large image",
        "Login form does not validate empty email field",
        "Unauthorized user can view other users' private data",
    ]
    cat_model, sev_model = load_classifiers()
    for bug in test_bugs:
        cat, sev = classify_bug(bug, cat_model, sev_model)
        print(f"'{bug}' -> Category: {cat}, Severity: {sev}")
