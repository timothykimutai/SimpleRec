from flask import Flask, request, jsonify, render_template
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask App
app = Flask(__name__)

# Load the Movies Data using TMDB API
api_key = "5d03b2f27c88738bd15573d4c3854a9a"
base_url = "https://api.themoviedb.org/3"

# Fetch genres mapping
genre_url = f"{base_url}/genre/movie/list?api_key={api_key}&language=en-US"
genre_response = requests.get(genre_url)
genre_data = genre_response.json()
genre_mapping = {genre['id']: genre['name'] for genre in genre_data['genres']}

# Fetch popular movies
url = f"{base_url}/movie/popular?api_key={api_key}&language=en-US&page=1"
response = requests.get(url)
data = response.json()

# Create DataFrame
movies_list = []
for movie in data["results"]:
    movie_id = movie["id"]
    title = movie["title"]
    rating = movie["vote_average"]
    popularity = movie["popularity"]
    genre_ids = movie["genre_ids"]
    genres = [genre_mapping.get(genre_id) for genre_id in genre_ids if genre_mapping.get(genre_id)]
    movies_list.append([movie_id, title, rating, popularity, genres])

movies_df = pd.DataFrame(movies_list, columns=["movie_id", "title", "rating", "popularity", "genres"])
movies_df["genre_str"] = movies_df["genres"].apply(lambda x: " ".join(x) if isinstance(x, list) else "")

# Vectorize genres
vectorizer = TfidfVectorizer()
genre_vectors = vectorizer.fit_transform(movies_df["genre_str"])
similarity_scores = cosine_similarity(genre_vectors)

# Recommendation Function
def recommend_movies(movie_title, num_recommendations=5):
    movie_title = movie_title.lower()
    # Find movie index with case-insensitive matching
    if movie_title not in movies_df['title'].str.lower().values:
        return ["No matching movie found."]
    
    movie_idx = movies_df[movies_df['title'].str.lower() == movie_title].index[0]
    similar_indices = similarity_scores[movie_idx].argsort()[-num_recommendations - 1:][::-1][1:]
    recommended_titles = movies_df.iloc[similar_indices]["title"].values.tolist()
    return recommended_titles if recommended_titles else ["No recommendations found."]

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
