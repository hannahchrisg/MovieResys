import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_reddit_reviews(movie_title):
    print(f"\n🔍 Searching Reddit for: {movie_title}")

    query = f"site:reddit.com {movie_title} movie review discussion opinions"

    results = client.search(query, max_results=2)

    all_results = []

    for r in results["results"]:
        all_results.append({
            "url": r["url"],
            "content": r["content"]
        })

    print(f"  ✓ {query}")

    return all_results