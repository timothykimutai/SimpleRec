# **Project Report: Movie Recommendation System**

**Table of Contents:**
1. Introduction
2. Objectives
3. Data Collection and Preprocessing
4. Exploratory Data Analysis (EDA)
5. Model Development
6. Model Evaluation
7. Deployment using Flask API
8. Frontend Development and Styling
9. Results and Discussion
10. Conclusion
11. Future Work

---

### **1. Introduction**

Recommender systems have become integral to modern applications, offering personalized suggestions to users based on their preferences. This project focuses on building a content-based movie recommendation system that suggests movies to users based on genre similarity.

I utilized The Movie Database (TMDb) API to fetch real-world movie data, developed a machine learning model to compute content similarity, and deployed the solution using Flask API.

### **2. Objectives**

The primary objectives of this project were:
- To develop a content-based movie recommendation system.
- To scrape movie data from the TMDb API.
- To implement text vectorization and similarity scoring for movie recommendations.
- To evaluate the recommendation model.
- To deploy the application using Flask and design a user-friendly frontend.

### **3. Data Collection and Preprocessing**

**Data Source:** TMDb API (https://www.themoviedb.org/)

#### **Data Extraction**
I fetched popular movies and genre information using TMDb API with the following steps:
1. **API Key Setup:** Secured an API key to access TMDb endpoints.
2. **Popular Movies Endpoint:** Fetched movie details, including movie IDs, titles, ratings, and genre IDs.
3. **Genre List Endpoint:** Extracted genre mappings.

**Data Fields:**
- Movie ID
- Title
- Rating
- Popularity
- Genres

**Data Cleaning:**
- Checked for missing values (none found).
- Converted `movie_id` to object data type.
- Combined genres into a single string for vectorization.

### **4. Exploratory Data Analysis (EDA)**

Key insights from the analysis:
- **Distribution of Ratings:** Visualized the distribution of ratings using Seaborn histograms.
- **Unique Movies:** Verified the number of unique movies.

Visualization Example:
```python
sns.histplot(movies_df['rating'], bins=10, kde=True)
plt.title("Distribution of Ratings")
plt.show()
```

### **5. Model Development**

**Text Vectorization:**
We employed TF-IDF vectorization to represent genre information.
```python
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
genre_vectors = vectorizer.fit_transform(movies_df['genre_str'])
```

**Cosine Similarity:**
Cosine similarity was computed to find similar movies.
```python
from sklearn.metrics.pairwise import cosine_similarity
similarity_scores = cosine_similarity(genre_vectors)
```

**Recommendation Function:**
The recommendation function retrieves the top five similar movies.
```python
def recommend_movies(movie_title, num_recommendations=5):
    if movie_title not in movies_df['title'].values:
        return f"'{movie_title}' not found in the dataset."
    movie_idx = movies_df[movies_df['title'] == movie_title].index[0]
    similar_indices = similarity_scores[movie_idx].argsort()[-num_recommendations - 1:][::-1][1:]
    return movies_df.iloc[similar_indices]['title'].values
```

### **6. Model Evaluation**

We evaluated the recommendation system using multiple metrics:

1. **Manual Evaluation:**
   - Tested with known movie titles and assessed the quality of recommendations.

2. **Precision and Recall:**
```python
def precision_at_k(recommended_movies, relevant_movies, k=5):
    relevant_hits = [movie for movie in recommended_movies[:k] if movie in relevant_movies]
    return len(relevant_hits) / k
```

3. **Mean Average Precision (MAP):**
Calculated to measure overall recommendation accuracy.

4. **Diversity Metric:**
Measured how diverse the recommended movies were.

### **7. Deployment using Flask API**

**Steps for Deployment:**
- Created a Flask application to handle API requests.
- Developed routes for fetching recommendations.
- Integrated the recommendation logic with the frontend.

Example of a Flask route:
```python
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    if request.method == 'POST':
        movie_title = request.form['movie_title']
        recommendations = recommend_movies(movie_title)
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
```

### **8. Frontend Development and Styling**

I designed a responsive and aesthetically pleasing frontend using HTML and CSS.

Key Design Features:
- Clean layout with user-friendly form inputs.
- Recommendations displayed in a stylish list format.
- Integrated animations and hover effects.

### **9. Results and Discussion**

**Evaluation Results:**
- Achieved high precision and reasonable diversity in recommendations.
- Successfully deployed the system with interactive user feedback.
- Users found the recommendations relevant based on the genres.

**Challenges:**
- Limited data for some obscure movies.
- Balancing recommendation diversity and precision.

### **10. Conclusion**

This project successfully developed and deployed a content-based movie recommendation system using real-world data from TMDb API. The system provides relevant and diverse recommendations based on genre similarity and demonstrates the utility of machine learning in personalizing user experiences.

### **11. Future Work**

To enhance the system, the following improvements are suggested:
- **Incorporate Collaborative Filtering:** Integrate user ratings for a hybrid recommendation approach.
- **Enhanced Model Evaluation:** Implement additional metrics such as novelty and serendipity.
- **User Authentication:** Allow users to save preferences and view personalized recommendations.
- **Improved UI/UX:** Add advanced search options and user interaction features.
- **Deployment on Cloud:** Host the application on a cloud service for wider accessibility.

---

**Appendix:**
- **Source Code:** Available in the project repository.
- **TMDb API Documentation:** https://developers.themoviedb.org/

