import pickle
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd


# ==========================================
# TMDB API
# ==========================================

API_KEY = "your_actual_key"

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


# ==========================================
# Session with retries (handles transient errors / rate limiting)
# ==========================================

session = requests.Session()

retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

session.mount("https://", HTTPAdapter(max_retries=retries))


# ==========================================
# Fetch Poster (cached + returns debug info)
# ==========================================

@st.cache_data(show_spinner=False, ttl=86400)
def fetch_poster(movie_id, movie_title):

    debug_info = []

    # ------------------------------------------
    # First: Get poster using movie ID
    # ------------------------------------------

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    try:

        response = session.get(
            url,
            params=params,
            timeout=10
        )

        debug_info.append(f"ID lookup status: {response.status_code}")

        if response.status_code == 200:

            data = response.json()

            poster_path = data.get("poster_path")

            if poster_path:

                return IMAGE_BASE_URL + poster_path, debug_info

            else:

                debug_info.append("ID found but poster_path is null in TMDB")

        else:

            debug_info.append(f"ID lookup response: {response.text[:200]}")

    except requests.exceptions.RequestException as e:

        debug_info.append(f"ID lookup error: {e}")


    # ------------------------------------------
    # If poster not found, search by movie title
    # ------------------------------------------

    search_url = "https://api.themoviedb.org/3/search/movie"

    search_params = {
        "api_key": API_KEY,
        "query": movie_title,
        "language": "en-US"
    }

    try:

        response = session.get(
            search_url,
            params=search_params,
            timeout=10
        )

        debug_info.append(f"Search status: {response.status_code}")

        if response.status_code == 200:

            data = response.json()

            results = data.get("results", [])

            debug_info.append(f"Search returned {len(results)} results")

            if results:

                poster_path = results[0].get("poster_path")

                if poster_path:

                    return IMAGE_BASE_URL + poster_path, debug_info

                else:

                    debug_info.append("Top search result has no poster_path")

        else:

            debug_info.append(f"Search response: {response.text[:200]}")

    except requests.exceptions.RequestException as e:

        debug_info.append(f"Search error: {e}")


    return None, debug_info


# ==========================================
# Load Movie Data
# ==========================================

movies_dict = pickle.load(
    open("movie_dict.pkl", "rb")
)

movies = pd.DataFrame(movies_dict)


# ==========================================
# Load Similarity Matrix
# ==========================================

similarity = pickle.load(
    open("similarity.pkl", "rb")
)


# ==========================================
# Recommendation Function
# ==========================================

def recommend(movie):

    movie_index = movies[
        movies["title"] == movie
    ].index[0]


    distances = sorted(
        list(
            enumerate(
                similarity[movie_index]
            )
        ),
        reverse=True,
        key=lambda x: x[1]
    )


    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_debug = []


    for i in distances[1:6]:

        movie_id = movies.iloc[i[0]]["movie_id"]

        movie_name = movies.iloc[i[0]]["title"]


        # Add movie name

        recommended_movie_names.append(
            movie_name
        )


        # Fetch poster

        poster, debug_info = fetch_poster(
            movie_id,
            movie_name
        )


        recommended_movie_posters.append(
            poster
        )

        recommended_movie_debug.append(
            debug_info
        )


    return (
        recommended_movie_names,
        recommended_movie_posters,
        recommended_movie_debug
    )


# ==========================================
# Streamlit UI
# ==========================================

st.title("🎬 Movie Recommender System")

st.write(
    "Select a movie and get 5 similar movie recommendations."
)


movie_list = movies["title"].values


selected_movie_name = st.selectbox(
    "Select a movie",
    movie_list
)


# ==========================================
# Recommend Button
# ==========================================

if st.button("Recommend"):


    names, posters, debug_infos = recommend(
        selected_movie_name
    )


    st.subheader("🍿 Recommended Movies")


    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [col1, col2, col3, col4, col5]


    for idx, col in enumerate(columns):

        with col:

            st.write(names[idx])

            if posters[idx]:

                st.image(
                    posters[idx],
                    use_container_width=True
                )

            else:

                st.write("Poster not available")

                with st.expander("Why?"):

                    for line in debug_infos[idx]:

                        st.caption(line)