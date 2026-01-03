import pickle
import streamlit as st
import requests
import os
import pandas as pd
import gdown
from design import load_css, header_section, movie_card


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="WatchWise | Movie Recommender",
    layout="wide"
)


# -------- Poster Fetch ----------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get("poster_path", None)
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/500x750?text=No+Image"


# -------- Load Movies ----------
BASE_DIR = os.path.dirname(__file__)
movies_path = os.path.join(BASE_DIR, "movies.pkl")
similarity_path = os.path.join(BASE_DIR, "similarity.pkl")

if os.path.exists(movies_path):
    movies = pickle.load(open(movies_path, "rb"))
else:
    try:
        movie_dict = pickle.load(open(os.path.join(BASE_DIR, "movie_dict.pkl"), "rb"))
        movies = pd.DataFrame(movie_dict)
    except FileNotFoundError:
        st.error("❌ Movie data files not found. Please ensure movies.pkl or movie_dict.pkl exists in the repository.")
        st.stop()


# -------- GOOGLE DRIVE DOWNLOAD (ONLY FIRST TIME) ----------
FILE_ID = "1XYrOW0T4OtZEZr-e000WEhj9-lVb22wA"
DRIVE_URL = f"https://drive.google.com/uc?id={FILE_ID}"

if not os.path.exists(similarity_path):
    st.info("⬇️ Downloading similarity matrix from Google Drive (only first time)... Please wait")
    try:
        gdown.download(DRIVE_URL, similarity_path, quiet=False)
        st.success("Similarity matrix downloaded successfully 🎉")
    except Exception as e:
        st.error("❌ Failed to download similarity file.")
        st.write(e)
        st.stop()

# Load similarity now
similarity = pickle.load(open(similarity_path, "rb"))


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
        except:
            continue

    return names, posters


# -------- UI ----------
load_css()
header_section()

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a Movie", movie_list)

if st.button("🔍 Show Recommendations", use_container_width=True):
    names, posters = recommend(selected_movie)

    if len(names) >= 5:
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                movie_card(name, poster)
    else:
        st.warning(f"⚠️ Only {len(names)} recommendations available")
