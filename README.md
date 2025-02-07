# **🎥 SimpleRec - Movie Recommendation System**

## 📖 Project Overview

SimpleRec is a Flask-based movie recommendation system that provides users with suggestions for movies based on their search inputs. The system fetches data from TMDB (The Movie Database) and displays interactive movie posters. Clicking on a poster redirects users to a streaming platform for easy access.

---

## 🚀 Features

- **Search Functionality:** Users can search for movies by title.
- **Interactive Recommendations:** Grid-based UI with clickable movie posters.
- **Navbar with Sidebar:** A stylish navigation bar featuring search, sign-in, and sidebar options.
- **Dynamic Data Fetching:** Movie details are fetched from TMDB API and displayed.
- **Responsive Design:** Mobile-friendly and attractive UI.

---

## 🛠️ Tech Stack

- **Frontend:** HTML, Bootstrap
- **Backend:** Flask
- **Data Fetching:** TMDB API
- **Recommendation Engine:** TF-IDF and cosine similarity
- **Deployment:** Local environment with Flask

---

## 🧩 Project Structure

```
├── app.py                  # Flask Application
├── templates
│   └── index.html           # Main Template for UI
├── static                   # CSS and JS Files
├── movies_data_optimized.csv # Optimized Movie Dataset
└── README.md                # Project Documentation
```

---

## 🛠️ Installation Guide

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)

### Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/timothykimutai/SimpleRec
   ```
2. Navigate into the project directory:
   ```bash
   cd simple-rec
   ```
3. Create and activate a virtual environment (optional):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Open the application in your browser:
   ```bash
   http://127.0.0.1:5000
   ```

---

## 🎯 Usage Instructions

- **Search:** Enter a movie title in the search bar and click search to view recommendations.
- **Interactive Grid:** Click on any movie poster to be directed to a streaming platform.
- **Sign In:** Use the sign-in button for potential user account features (pending development).

---

## 📊 Recommendation Engine Details

The recommendation system uses the following approach:

1. **Data Fetching:**

   - Fetches popular movies from TMDB API.
   - Stores and processes movie details such as title, genres, and overview.

2. **Feature Extraction:**

   - Combines genres, overview, and release date for vectorization.

3. **Vectorization:**

   - Utilizes TF-IDF vectorizer to represent movie features.

4. **Similarity Calculation:**

   - Computes cosine similarity using `linear_kernel` to find similar movies.

---

## 📷 Screenshots

**Search and Recommendations Page:**

**Navbar and Sidebar:**

---

## 📚 Acknowledgments

- [TMDB API](https://www.themoviedb.org/) for providing the movie data.
- Bootstrap for beautiful frontend components.
- Flask for creating the backend.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👏 Contributing

Contributions are welcome! Feel free to fork the project and submit pull requests.

---

## 🔗 Contact

If you have any questions or suggestions, please reach out at timothykimtai\@gmail.com

