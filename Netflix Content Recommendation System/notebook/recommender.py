from pathlib import Path
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Dataset
DATA_PATH = BASE_DIR / "Dataset.csv"

df = pd.read_csv(DATA_PATH)


# Features
features = [
    'type',
    'director',
    'country',
    'rating',
    'listed_in'
]

for feature in features:
    df[feature] = df[feature].fillna('')


# Combine features
df['combined_features'] = (
    df['type'] + ' ' +
    df['director'] + ' ' +
    df['country'] + ' ' +
    df['rating'] + ' ' +
    df['listed_in']
)


# TF-IDF
tfidf = TfidfVectorizer(
    stop_words='english'
)

tfidf_matrix = tfidf.fit_transform(
    df['combined_features']
)


# Similarity
similarity_matrix = cosine_similarity(
    tfidf_matrix
)


# Title index
indices = pd.Series(
    df.index,
    index=df['title']
).drop_duplicates()


# Recommendation function
def recommend(title, num_recommendations=5):

    if title not in indices:
        return pd.DataFrame()

    idx = indices[title]

    similarity_scores = list(
        enumerate(similarity_matrix[idx])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    similarity_scores = similarity_scores[
        1:num_recommendations + 1
    ]

    movie_indices = [
        i[0] for i in similarity_scores
    ]

    recommendations = df.iloc[movie_indices][
        ['title', 'type', 'listed_in', 'rating']
    ].copy()

    recommendations['similarity_score'] = [
        round(score, 3)
        for _, score in similarity_scores
    ]

    return recommendations