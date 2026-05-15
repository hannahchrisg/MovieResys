import pandas as pd
import glob
import re

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

import joblib

print("ML environment ready!")

# -----------------------------
# PART 1 — TRAIN SENTIMENT MODEL
# -----------------------------

reviews = pd.read_csv("IMDB Dataset.csv")

def clean_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = text.lower()
    return text

reviews["review"] = reviews["review"].apply(clean_text)

vector = TfidfVectorizer(max_features=5000)
X = vector.fit_transform(reviews["review"])
y = reviews["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Sentiment Model Accuracy:", accuracy_score(y_test, y_pred))

joblib.dump(model, "sentiment_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("Model saved successfully!")


# -----------------------------
# PART 2 — LOAD MOVIE DATASET
# -----------------------------

files = glob.glob("tmdb-movies-*.json")

df_list = []

for file in files:
    df = pd.read_json(file, lines=True)
    df_list.append(df)

movies = pd.concat(df_list, ignore_index=True)

print("Total movies:", movies.shape)

# Remove duplicates
movies = movies.drop_duplicates(subset="id_imdb")

# Filter low quality movies
movies = movies[movies["vote_count"] > 50]
movies = movies[movies["vote_average"] > 0]

print("Movies after cleaning:", movies.shape)


# -----------------------------
# PART 3 — MOVIE RANKING SYSTEM
# -----------------------------

movies["popularity_norm"] = movies["popularity"] / movies["popularity"].max()
movies["vote_count_norm"] = movies["vote_count"] / movies["vote_count"].max()

movies["final_score"] = (
    movies["vote_average"] * 0.5 +
    movies["vote_count_norm"] * 5 * 0.3 +
    movies["popularity_norm"] * 10 * 0.2
)

movies = movies.sort_values(by="final_score", ascending=False)


# -----------------------------
# PART 4 — GENRE CONVERSION
# -----------------------------

genre_map = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

def convert_genres(genre_list):
    return [genre_map.get(g) for g in genre_list if g in genre_map]

movies["genre_names"] = movies["genre_ids"].apply(convert_genres)


# -----------------------------
# PART 5 — USER GENRE INPUT
# -----------------------------

user_genre = input("Enter a genre: ").strip().lower()

filtered_movies = movies[
    movies["genre_names"].apply(
        lambda genres: any(user_genre == g.lower() for g in genres) if genres else False
    )
]

top_movies = filtered_movies.sort_values(
    by="final_score", ascending=False
).head(10)

print("\nTop Movies:\n")
print(top_movies[["title", "genre_names", "final_score"]])


# -----------------------------
# PART 6 — TEST SENTIMENT MODEL
# -----------------------------

def predict_sentiment(text):

    text = clean_text(text)
    text_vector = vector.transform([text])
    prediction = model.predict(text_vector)

    return prediction[0]


test_comment = "This movie was absolutely amazing with great acting!"

result = predict_sentiment(test_comment)

print("\nTest Comment Sentiment:")
print("Comment:", test_comment)
print("Predicted sentiment:", result)


# Save cleaned dataset
movies.to_csv("cleaned_movies.csv", index=False)

print("\nCleaned dataset saved!")