import pickle
import streamlit as st
import requests
import os
import pandas as pd
from Design import load_css, header_section, movie_card


# -------- Poster Fetch ----------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + poster_path


# -------- Load Data ----------
BASE_DIR = os.path.dirname(__file__)
movies_path = os.path.join(BASE_DIR, "movies.pkl")

if os.path.exists(movies_path):
    movies = pickle.load(open(movies_path, "rb"))
else:
    movie_dict = pickle.load(open(os.path.join(BASE_DIR, "movie_dict.pkl"), "rb"))
    movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open(os.path.join(BASE_DIR, "similarity.pkl"), "rb"))


# -------- Recommendation ----------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        posters.append(fetch_poster(movie_id))
        names.append(movies.iloc[i[0]].title)

    return names, posters


# -------- UI ----------
st.set_page_config(page_title="WatchWise | Movie Recommender", layout="wide")

load_css()
header_section()

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a Movie", movie_list)

if st.button("🔍 Show Recommendations", use_container_width=True):
    names, posters = recommend(selected_movie)

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
