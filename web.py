import streamlit as st
import pickle
import requests   # To hit the API
# to run the file, write: streamlit run <filename>
similarity = pickle.load(open('similarity.pkl', 'rb'))  # This will give back the similarity array that we dumped
movies_df = pickle.load(open('movies.pkl', 'rb'))  # Opening in read binary mode. Will give us back our dataframe that we dumped
movies_list = movies_df['title'].values  # Accessing the new_df dataframe and getting the movies(present in title column)

def fetch_poster(movie_id):
     response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=40cb915095a5c52bb85d7d1b9b3a0190&language=en-US')
     data = response.json()   # Converting it to JSON
     return 'http://image.tmdb.org/t/p/w500/' + data['poster_path']

def recommend(movie):
     movie_index = movies_df[movies_df['title'] == movie].index[0]
     distances = similarity[movie_index]
     top_5 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

     recommended_movies = []
     recommended_movies_posters = []
     for i in top_5:
          movie_id = movies_df.iloc[i[0]].movie_id   # To fetch poster from API
          recommended_movies.append(movies_df.iloc[i[0]].title)
          recommended_movies_posters.append(fetch_poster(movie_id))
     return recommended_movies, recommended_movies_posters


st.title('Movie Recommender System')
st.text('(By Ammish Tandon)')
movie_selected = st.selectbox(
     'Choose a Movie:',
     movies_list)

if st.button('Recommend'):   # Creating a button with name Recommend
     names, posters = recommend(movie_selected)
     col1, col2, col3, col4, col5 = st.columns(5)

     with col1:
          st.text(names[0])
          st.image(posters[0])

     with col2:
          st.text(names[1])
          st.image(posters[1])

     with col3:
          st.text(names[2])
          st.image(posters[2])

     with col4:
          st.text(names[3])
          st.image(posters[3])

     with col5:
          st.text(names[4])
          st.image(posters[4])