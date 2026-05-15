from flask import Flask, render_template, request
import pandas as pd
import ast
import os
import requests
from dotenv import load_dotenv
from reddit_search import search_reddit_reviews
from recommender import analyse_movie

load_dotenv()

app = Flask(__name__)

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")

def get_movie_poster(title):
    # Try TMDB first if key exists
    if TMDB_API_KEY:
        try:
            r = requests.get(
                "https://api.themoviedb.org/3/search/movie",
                params={"api_key": TMDB_API_KEY, "query": title},
                timeout=5
            )
            data = r.json()
            if data.get("results"):
                poster = data["results"][0].get("poster_path")
                if poster:
                    return TMDB_IMAGE_BASE + poster
        except:
            pass

    # Fallback — use OMDb (free, no key needed for basic use)
    try:
        r = requests.get(
            "https://www.omdbapi.com/",
            params={"t": title, "apikey": "trilogy"},
            timeout=5
        )
        data = r.json()
        poster = data.get("Poster", "")
        if poster and poster != "N/A":
            return poster
    except:
        pass

    # Final fallback
    return f"https://via.placeholder.com/300x450/1a1a1a/ff6b35?text={title.replace(' ', '+')}"
def get_top_movies(genre, count=6):
    movies = pd.read_csv("cleaned_movies.csv")

    def parse_genres(val):
        try:
            if isinstance(val, str):
                val = ast.literal_eval(val)
            return [g.lower() for g in val if g]
        except:
            return []

    movies["genre_names"] = movies["genre_names"].apply(parse_genres)
    filtered = movies[
        movies["genre_names"].apply(lambda g: genre.lower() in g)
    ]
    return filtered.sort_values("final_score", ascending=False).head(count)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", movies=None, genre="")

@app.route("/recommend", methods=["POST"])
def recommend():
    genre = request.form.get("genre", "").strip().title()
    top_movies = get_top_movies(genre)

    if top_movies.empty:
        return render_template("index.html", movies=[], genre=genre)

    results = []
    for _, row in top_movies.iterrows():
        title = row["title"]
        poster = get_movie_poster(title)
        reddit_results = search_reddit_reviews(title)
        analysis = analyse_movie(title, reddit_results)

        good, bad, pos_snippets, neg_snippets = [], [], [], []
        lines = analysis.split("\n")
        section = None
        for line in lines:
            line = line.strip()
            if "WHAT PEOPLE LOVE" in line:
                section = "good"
            elif "WHAT PEOPLE DISLIKE" in line:
                section = "bad"
            elif "POSITIVE SNIPPETS" in line:
                section = "pos_snippets"
            elif "NEGATIVE SNIPPETS" in line:
                section = "neg_snippets"
            elif line.startswith("•") and section == "good":
                good.append(line[1:].strip())
            elif line.startswith("•") and section == "bad":
                bad.append(line[1:].strip())
            elif line.startswith("•") and section == "pos_snippets":
                pos_snippets.append(line[1:].strip())
            elif line.startswith("•") and section == "neg_snippets":
                neg_snippets.append(line[1:].strip())

        results.append({
            "title": title,
            "poster": poster,
            "score": round(row["final_score"], 2),
            "good": good,
            "bad": bad,
            "pos_snippets": pos_snippets,
            "neg_snippets": neg_snippets,
            "full_analysis": analysis,
            "sources": [r["url"] for r in reddit_results[:3]]
        })

    return render_template("index.html", movies=results, genre=genre)

if __name__ == "__main__":
    app.run(debug=True)