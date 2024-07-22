import pickle
import streamlit as st
import requests
from streamlit.components.v1 import html
st.set_page_config(page_title="Movie Recommendation System", layout='wide')


st.title("Movie Recommendation System")

movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

def fetch_movie_info(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    title = data['title']
    release_date = data['release_date']
    overview = data['overview']
    info = f"{title}\nRelease Date:{release_date}\n{overview}"
    return full_path, info

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_infos = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, info = fetch_movie_info(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_infos.append(info)
    return recommended_movie_names, recommended_movie_posters, recommended_movie_infos

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_infos = recommend(selected_movie)
    cols = st.columns(5)
    for col, name, poster, info in zip(cols, recommended_movie_names, recommended_movie_posters, recommended_movie_infos):
        with col:
            st.text(name)
            html(f'<img src="{poster}" title="{info}" style="width:100%">', height=400)