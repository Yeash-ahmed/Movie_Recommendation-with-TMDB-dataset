import streamlit as st

def load_css():
    st.markdown("""
        <style>

        body {
            background:#000000;
        }

        .main-header {
            text-align:center;
            font-size:42px;
            font-weight:900;
            color:#ffffff;
            letter-spacing:2px;
            margin-bottom:5px;
        }

        .brand {
            color:#e50914;
        }

        .sub-text {
            text-align:center;
            color:#b3b3b3;
            margin-bottom:50px;
            font-size:16px;
        }

        .movie-card {
            background: linear-gradient(145deg, rgba(20,20,20,0.9), rgba(10,10,10,0.8));
            border-radius:18px;
            padding:12px;
            text-align:center;
            border:1px solid #1f1f1f;
            transition:0.3s;
            box-shadow:0px 0px 25px rgba(229, 9, 20, 0.15);
        }

        .movie-card:hover {
            transform: scale(1.05);
            border:1px solid #e50914;
            box-shadow:0px 0px 35px rgba(229, 9, 20, 0.4);
        }

        .movie-name {
            color:#ffffff;
            font-size:16px;
            margin-top:10px;
            font-weight:700;
        }

        .selectbox-label {
            color:white;
            font-size:18px;
            font-weight:600;
        }

        </style>
    """, unsafe_allow_html=True)


def header_section():
    st.markdown("<div class='main-header'>Watch<span class='brand'>Wise</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Your Personal AI Powered Smart Movie Recommendation System 🎬</div>", unsafe_allow_html=True)


def movie_card(name, poster):
    st.markdown(f"""
        <div class="movie-card">
            <img src="{poster}" width="200" style="border-radius:14px;">
            <div class="movie-name">{name}</div>
        </div>
    """, unsafe_allow_html=True)
