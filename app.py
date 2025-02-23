import streamlit as st
import joblib
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TMDB_TOKEN")

movies = joblib.load(open('movies_list.joblib', 'rb'))
similarity = joblib.load(open('similarity.joblib', 'rb'))
movies_list = movies['title'].values


def recommend(movie):
    index = movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda vector:vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetchPoster(movies_id))
    return recommend_movie,recommend_poster

def fetchPoster(mov):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key='+ token
    url = url.format(mov)
    data = requests.get(url)
    data = data.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']
        
st.set_page_config(layout='wide',page_title='Movie Recommender System',page_icon='🎬')     
st.header("Movie Recommender System")
selected = st.selectbox("select a movie", movies_list)

if st.button("Show Recommend"):
    movieName,moviesPoster=recommend(selected)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(movieName[0])
        st.image(moviesPoster[0])
    with col2:
        st.text(movieName[1])
        st.image(moviesPoster[1])
    with col3:
        st.text(movieName[2])
        st.image(moviesPoster[2])
    with col4:
        st.text(movieName[3])
        st.image(moviesPoster[3])
    with col5:
        st.text(movieName[4])
        st.image(moviesPoster[4])