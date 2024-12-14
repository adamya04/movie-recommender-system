import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=49c64c3757fc4da03d66b3e85a0d5df4&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return None  # Return None if no poster is found


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters



movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('Movie Recommender')


st.sidebar.header('Select a Movie')
selected_movie_name = st.sidebar.selectbox('Choose your movie of choice:', movies['title'].values)

# Recommendation button
if st.sidebar.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    # Display recommendations in a grid layout
    st.subheader('Recommended Movies:')
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(recommended_movie_posters[i], width=200)  # Set image width
            st.text(recommended_movie_names[i])

# Footer
st.markdown("""
    ---
    Made with ❤️ by Adamya Sharma
    
""")
