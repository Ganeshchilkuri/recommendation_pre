import pickle
import streamlit as st
import pandas as pd
import requests
import difflib
global arr
arr = {
    'names' :[" "],
    'overview' :[" "]
}
arr = pd.DataFrame(arr)
def fetch_poster(movie_id):
    url = "https://imdb146.p.rapidapi.com/v1/find/"

    querystring = {"query":movie_id}

    headers = {
	    "X-RapidAPI-Key": "c56d5b6c1fmsh7d42889a4b5024dp12aafdjsncbca94223452",
	    "X-RapidAPI-Host": "imdb146.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    poster_path = data["titleResults"]["results"][0]['titlePosterImageModel']['url']
    return poster_path

def recommend(movie):
    list_of_all_titles = movie_list['names'].tolist()       # get all movie name as list

    find_close_match = difflib.get_close_matches(movie, list_of_all_titles)  # find closest match --list of movie-- form oru given movie
    print(" similiar names  :  ",  find_close_match ,"\n\n")

    close_match = find_close_match[0]             # we take first one which is given by cloest movie

    index_of_the_movie = movie_list[movie_list.names == close_match]['index'].values[0]   #  geting the index of the movie

    similarity_score = list(enumerate(similarity[index_of_the_movie]))            # generate the similarity score for the given movie
        
    sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True)     # sort the score to get top 10 more similiarty movies

    print('Movies suggested for you : \n')

    i = 1

    # print the top 10 movies base on similiarity score 
    recommended_movie_names = []
    # recommended_movie_posters = []
    overview = []
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movie_list[movie_list.index==index]['names'].values[0]
        overview_from_index = movie_list[movie_list.index==index]['overview'].values[0]
        if (i<=10):
            recommended_movie_names.append(title_from_index)
            overview.append(overview_from_index)
            # recommended_movie_posters.append(fetch_poster(title_from_index))
            i+=1
    
    return recommended_movie_names,overview


st.header('Movie Recommender System')
movies = pickle.load(open('recommend_data.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = pd.DataFrame(movies)
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list['names'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names,overview,recommended_movie_posters= recommend(selected_movie)
    for i in range(10):
        with st.container():
            col1,col2 = st.columns([0.4,0.6],gap="medium")
            with col1:
                st.title(recommended_movie_names[i])
                st.image("https://static.streamlit.io/examples/cat.jpg")
            with col2:
                st.subheader("Description")
                st.write(overview[i])           


