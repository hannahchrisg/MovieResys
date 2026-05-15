import os
from groq import Groq
from dotenv import load_dotenv
from reddit_search import search_reddit_reviews

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyse_movie(movie_title, results):
    print(f"\n🧠 Analysing reviews for: {movie_title}")
    
    all_text = ""
    for r in results[:6]:
        all_text += f"\n--- Reddit Result ---\n{r['content']}\n"
    
    all_text = all_text[:5000]
    
    prompt = f"""You are a movie review analyst. Based on these Reddit comments about "{movie_title}", extract real sentences.

IMPORTANT: Use exactly • as bullet points, nothing else.

Format your response exactly like this:

🎬 MOVIE: {movie_title}

⭐ OVERALL VERDICT
[One sentence summary of general Reddit opinion]

👍 WHAT PEOPLE LOVE
- [positive point 1]
- [positive point 2]
- [positive point 3]

👎 WHAT PEOPLE DISLIKE
- [negative point 1]
- [negative point 2]
- [negative point 3]

✂️ POSITIVE SNIPPETS
- [copy exact short phrase from the Reddit text below that shows praise]
- [copy exact short phrase from the Reddit text below that shows praise]
- [copy exact short phrase from the Reddit text below that shows praise]

✂️ NEGATIVE SNIPPETS
- [copy exact short phrase from the Reddit text below that shows criticism]
- [copy exact short phrase from the Reddit text below that shows criticism]

🎯 WATCH IT IF YOU LIKE
[type of viewer this movie suits]

---
Reddit data:
{all_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    
    return response.choices[0].message.content

def recommend_by_genre(genre):
    print(f"\n🎬 Finding top {genre} movies from your dataset...")
    
    import pandas as pd
    import ast

    movies = pd.read_csv("cleaned_movies.csv")
    
    # Parse genre names
    def parse_genres(val):
        try:
            if isinstance(val, str):
                val = ast.literal_eval(val)
            return [g.lower() for g in val if g]
        except:
            return []
    
    movies["genre_names"] = movies["genre_names"].apply(parse_genres)
    
    # Filter by genre
    filtered = movies[
        movies["genre_names"].apply(
            lambda g: genre.lower() in g
        )
    ]
    
    top = filtered.sort_values("final_score", ascending=False).head(5)
    
    if top.empty:
        print(f"❌ No movies found for genre: {genre}")
        return
    
    print(f"\n✅ Top {genre} movies found — fetching Reddit reviews...\n")
    print("="*50)
    
    for _, row in top.iterrows():
        title = row["title"]
        results = search_reddit_reviews(title)
        analysis = analyse_movie(title, results)
        print(f"\n{analysis}")
        
        print("\n📌 RAW REDDIT SOURCES USED:")
        for i, r in enumerate(results[:6], 1):
            print(f"\n  [{i}] {r['url']}")
            print(f"      {r['content'][:200]}...")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    genre = input("Enter a genre (e.g. Horror, Comedy, Action): ").strip()
    recommend_by_genre(genre)