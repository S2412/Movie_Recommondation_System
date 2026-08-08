
# 🎬 Movie Recommendation System

A content-based Movie Recommendation System built using **Python, Pandas, Streamlit, and the TMDB API**.

The application recommends 5 movies similar to the movie selected by the user and dynamically fetches movie posters from TMDB.

---

## 🚀 Features

* 🎬 Select a movie from a dropdown
* 🤖 Recommend 5 similar movies
* 🧠 Uses a precomputed similarity matrix
* 🖼️ Fetches movie posters using TMDB API
* 🔄 Searches posters using both movie ID and movie title
* ⚡ Uses Streamlit caching to reduce unnecessary API requests
* 🔁 Retry mechanism for temporary API failures
* 🐛 Debug information when a poster cannot be found
* 🌐 Interactive web interface using Streamlit

---

## 🛠️ Technologies Used

* Python
* Pandas
* Pickle
* Streamlit
* Requests
* TMDB API
* Scikit-learn
* Cosine Similarity

---

## 📂 Project Structure

```text
movie-recommender/
│
├── app.py
├── movie_dict.pkl
├── similarity.pkl
├── README.md

```

---

## 🧠 How It Works

The recommendation system follows these steps:

```text
User selects a movie
        ↓
Find movie index
        ↓
Get similarity scores
        ↓
Sort similarity scores
        ↓
Select top 5 similar movies
        ↓
Get movie IDs and titles
        ↓
Fetch posters from TMDB API
        ↓
Display recommendations
```

---

## 🔍 Recommendation Technique

This project uses **Content-Based Filtering**.

A similarity matrix is used to measure how similar movies are to each other.

The system finds the selected movie in the dataset and retrieves its similarity scores.

The movies with the highest similarity scores are recommended.

### Example

If the user selects:

```text
Inception
```

The system may recommend:

```text
Interstellar
The Prestige
Shutter Island
Tenet
The Matrix
```

---

## 🖼️ TMDB API

The application uses the **TMDB API** to fetch movie posters.

The process is:

```text
Movie ID
   ↓
TMDB Movie API
   ↓
poster_path
   ↓
TMDB Image URL
   ↓
Movie Poster
```

If the poster cannot be found using the movie ID, the application searches for the movie by title.

---

## ⚡ Caching

Streamlit's `st.cache_data()` is used to cache poster results.

The cache is configured for 24 hours.

This helps:

* Reduce unnecessary API requests
* Improve application performance
* Avoid repeatedly requesting the same poster


Run:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📊 Dataset

The project uses saved pickle files:

```text
movie_dict.pkl
similarity.pkl
```

### `movie_dict.pkl`

Contains movie information such as:

* Movie title
* Movie ID
* Other movie features

### `similarity.pkl`

Contains the precomputed similarity scores used for recommendations.

---

