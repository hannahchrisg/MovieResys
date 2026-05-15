import pandas as pd
import glob

print("Combining TMDB movie files...")

# Find all yearly movie files
files = glob.glob("tmdb-movies-*.json")

df_list = []

for file in files:
    print("Loading:", file)
    
    # IMPORTANT: lines=True because each line is a JSON object
    df = pd.read_json(file, lines=True)
    
    df_list.append(df)

# Combine all files
movies = pd.concat(df_list, ignore_index=True)

print("\nTotal movies loaded:", movies.shape)


# Remove duplicate movies
movies = movies.drop_duplicates(subset="id_imdb")

print("After removing duplicates:", movies.shape)


# Remove low quality movies
movies = movies[movies["vote_count"] > 50]
movies = movies[movies["vote_average"] > 0]

print("After filtering low quality movies:", movies.shape)


# Normalize popularity
movies["popularity_norm"] = movies["popularity"] / movies["popularity"].max()

# Normalize vote count
movies["vote_count_norm"] = movies["vote_count"] / movies["vote_count"].max()


# Create ranking score
movies["final_score"] = (
    movies["vote_average"] * 0.5 +
    movies["vote_count_norm"] * 5 * 0.3 +
    movies["popularity_norm"] * 10 * 0.2
)


# Sort movies by ranking score
movies = movies.sort_values(by="final_score", ascending=False)


print("\nTop Movies After Ranking:\n")

print(movies[[
    "title",
    "vote_average",
    "vote_count",
    "popularity",
    "final_score"
]].head(10))


# Save cleaned dataset
movies.to_csv("cleaned_movies.csv", index=False)

print("\nCleaned dataset saved as: cleaned_movies.csv")