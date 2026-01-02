import pickle
import streamlit as st
import requests
import os
import pandas as pd
from design import load_css, header_section, movie_card


# -------- Poster Fetch ----------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + poster_path


# -------- Load Data ----------
BASE_DIR = os.path.dirname(__file__)
movies_path = os.path.join(BASE_DIR, "movies.pkl")
similarity_path = os.path.join(BASE_DIR, "similarity.pkl")

# Load movies
if os.path.exists(movies_path):
    movies = pickle.load(open(movies_path, "rb"))
else:
    try:
        movie_dict = pickle.load(open(os.path.join(BASE_DIR, "movie_dict.pkl"), "rb"))
        movies = pd.DataFrame(movie_dict)
    except FileNotFoundError:
        st.error("❌ Movie data files not found. Please ensure movies.pkl or movie_dict.pkl exists in the repository.")
        st.stop()

# Load similarity matrix with better error handling
if os.path.exists(similarity_path):
    similarity = pickle.load(open(similarity_path, "rb"))
else:
    st.error("❌ Similarity matrix (similarity.pkl) not found.")
    st.info("To fix this:\n"
            "1. Make sure `similarity.pkl` is committed to your GitHub repository\n"
            "2. If the file is too large (>100MB), use Git LFS\n"
            "3. Or regenerate the similarity matrix using your training script")
    st.stop()


# -------- Recommendation ----------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        try:
            posters.append(fetch_poster(movie_id))
            names.append(movies.iloc[i[0]].title)
        except Exception as e:
            st.warning(f"Could not fetch poster for movie ID {movie_id}")
            continue

    return names, posters


# -------- UI ----------
st.set_page_config(page_title="WatchWise | Movie Recommender", layout="wide")

load_css()
header_section()

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a Movie", movie_list)

if st.button("🔍 Show Recommendations", use_container_width=True):
    names, posters = recommend(selected_movie)

    if len(names) >= 5:
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            movie_card(names[0], posters[0])
        with col2:
            movie_card(names[1], posters[1])
        with col3:
            movie_card(names[2], posters[2])
        with col4:
            movie_card(names[3], posters[3])
        with col5:
            movie_card(names[4], posters[4])
    else:
        st.warning(f"⚠️ Could only fetch {len(names)} recommendations instead of 5")
