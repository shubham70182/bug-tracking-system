# Bug Tracking System

A simple Python + SQLite bug tracker with ML-based auto-classification of bug category and severity.

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

Bug Tracking System is a command-line application for logging and managing software bugs. When you log a new bug, it uses a scikit-learn text classification pipeline to automatically suggest a **category** (UI, Backend, Database, Performance, Security) and a **severity** (Low, Medium, High) based on the bug description, which you can accept or override. Bugs are persisted to a local SQLite database, and you can view/filter them by status and see a summary of bug counts by category.

## How It Works

The classifier (`src/classifier.py`) uses two independent scikit-learn pipelines — one for category, one for severity — each built as:

```
TfidfVectorizer(stop_words="english") -> MultinomialNB()
```

The bug description is vectorized with TF-IDF (term frequency–inverse document frequency) and fed into a Multinomial Naive Bayes classifier. Both pipelines are trained on the same small, hand-labeled set of ~25 example bug descriptions defined directly in `classifier.py`, covering five categories (UI, Backend, Database, Performance, Security) and three severity levels (Low, Medium, High).

On first run, `load_classifiers()` checks for saved models in `models/`; if they don't exist, it trains fresh ones via `train_classifiers()` and saves them with `joblib`. Every time you log a new bug, `classify_bug()` runs the description through both pipelines to predict a category and severity, which are shown to you before the bug is saved.

## Project Structure

```
bug-tracking-system/
├── data/
│   └── bugs.db              # SQLite database (created at runtime, gitignored)
├── models/
│   ├── category_model.pkl   # Trained category classifier (gitignored)
│   └── severity_model.pkl   # Trained severity classifier (gitignored)
├── src/
│   ├── classifier.py        # TF-IDF + Naive Bayes training/prediction
│   ├── db.py                 # SQLite schema + CRUD operations
│   └── main.py                # CLI entry point
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

```bash
git clone https://github.com/shubham70182/bug-tracking-system.git
cd bug-tracking-system
pip install -r requirements.txt
```

## Usage

Run the CLI from the project root:

```bash
python src/main.py
```

The database and classifiers are initialized automatically on first run.

### Sample interaction

```
Bug Tracking System
====================
1. Log a new bug
2. View bugs
3. Update bug status
4. Summary by category
5. Exit

Choose an option: 1
Bug title: Login button unresponsive
Description: App crashes when clicking submit button on login page

Auto-classified as -> Category: UI, Severity: High
Accept classification? (y/n): y
Bug #1 logged successfully.
```

## Features

- **Log a new bug** — enter a title and description; the classifier auto-suggests category and severity, which you can accept or manually override.
- **View bugs** — list all bugs, or filter by status (Open / In Progress / Resolved).
- **Update bug status** — change a bug's status by ID.
- **Summary by category** — see a count of logged bugs grouped by category.

## Tech Stack

- **Python** — core application logic
- **SQLite** — lightweight local storage for bug records
- **scikit-learn** — TF-IDF vectorization and Naive Bayes classification

## Limitations / Note

The classifier is trained on a small (~25-example) hand-labeled dataset defined in-code. This is intentionally simple — it's meant to demonstrate a working ML classification pipeline, not to be production-accurate. Predictions on descriptions that differ significantly from the training examples may be unreliable.

## Future Improvements

- Expand the training dataset with a larger, more diverse set of labeled bugs
- Add a web UI (e.g. Flask/FastAPI + a simple frontend) instead of the CLI
- Expose a REST API for programmatic bug logging and querying
- Persist and retrain the classifier as new bugs are confirmed/corrected by users

## Author

**Shubham Rathore**
GitHub: [@shubham70182](https://github.com/shubham70182)

## License

This project is licensed under the MIT License — see below for details.

```
MIT License

Copyright (c) 2026 Shubham Rathore

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
