from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from joblib import Parallel, delayed
from functools import lru_cache
from fuzzywuzzy import process

# Initialize Flask App
app = Flask(__name__)

# API configuration
api_key = "5d03b2f27c88738bd15573d4c3854a9a"
base_url = "https://api.themoviedb.org/3"
genre_url = f"{base_url}/genre/movie/list?api_key={api_key}&language=en-US"

# Fetch genres mapping
genre_response = requests.get(genre_url)
genre_data = genre_response.json()
genre_mapping = {genre['id']: genre['name'] for genre in genre_data['genres']}

# Fetch movies from multiple pages using parallel requests
def fetch_movie_page(page):
    url = f"{base_url}/movie/popular?api_key={api_key}&language=en-US&page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

# Fetch data concurrently for 100 pages
all_results = Parallel(n_jobs=8)(delayed(fetch_movie_page)(page) for page in range(1, 101))
flat_results = [movie for page_result in all_results for movie in page_result]

# Process and store movie details
movies_list = []
for movie in flat_results:
    movie_id = movie["id"]
    title = movie["title"]
    rating = movie["vote_average"]
    popularity = movie["popularity"]
    genre_ids = movie["genre_ids"]
    genres = [genre_mapping.get(genre_id) for genre_id in genre_ids if genre_mapping.get(genre_id)]
    overview = movie.get("overview", "")
    release_date = movie.get("release_date", "")
    poster_path = movie.get("poster_path", "")
    movies_list.append([movie_id, title, rating, popularity, genres, overview, release_date, poster_path])
    


# Create DataFrame
movies_df = pd.DataFrame(
    movies_list,
    columns=["movie_id", "title", "rating", "popularity", "genres", "overview", "release_date", "poster_path"]
)
movies_df["genre_str"] = movies_df["genres"].apply(lambda x: " ".join(x) if isinstance(x, list) else "")

# Save data to CSV for persistence
movies_df.to_csv("movies_data_optimized.csv", index=False)

# Load data from CSV
movies_df = pd.read_csv("movies_data_optimized.csv")

# Replace NaN values with empty strings in text columns
movies_df.fillna("", inplace=True)

# Combine features for vectorization
movies_df["combined_features"] = (
    movies_df["genre_str"] + " " +
    movies_df["overview"] + " " +
    movies_df["release_date"].str[:4]  # Include release year
)

# Vectorize combined features
vectorizer = TfidfVectorizer(stop_words="english")
feature_vectors = vectorizer.fit_transform(movies_df["combined_features"])

# Compute cosine similarity using linear_kernel
similarity_scores = linear_kernel(feature_vectors, feature_vectors)

# Recommendation Function with Caching
@lru_cache(maxsize=1000)
def recommend_movies(movie_title: str, num_recommendations: int = 10):
    movie_title = movie_title.lower()

    # Find the closest matching title
    possible_matches = movies_df['title'].str.lower().tolist()
    best_match, score = process.extractOne(movie_title, possible_matches)
    if score < 50:  # Threshold for match confidence
        return ["No matching movie found."]

    movie_idx = movies_df[movies_df['title'].str.lower() == best_match].index[0]
    similar_indices = np.argpartition(-similarity_scores[movie_idx], num_recommendations + 1)[:num_recommendations + 1]
    similar_indices = similar_indices[np.argsort(-similarity_scores[movie_idx][similar_indices])][1:]

    recommendations = []
    for idx in similar_indices:
        movie = movies_df.iloc[idx]
        recommendations.append({
            "title": movie["title"],
            "poster_path": movie["poster_path"],
            "rating": movie["rating"],
            "release_date": movie["release_date"]
        })

    return recommendations if recommendations else ["No recommendations found."]

# API Routes
@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    if request.method == "POST":
        movie_title = request.form["movie_title"]
        recommendations = recommend_movies(movie_title)
    return render_template("index.html", recommendations=recommendations)

@app.route("/api/recommendations", methods=["GET"])
def api_recommendations():
    movie_title = request.args.get("movie_title")
    recommendations = recommend_movies(movie_title)
    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
