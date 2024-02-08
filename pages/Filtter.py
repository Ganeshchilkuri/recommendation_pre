import streamlit as st
import pandas as pd
import pickle
import requests
movies = pickle.load(open('recommend_data.pkl','rb'))
movie_list = pd.DataFrame(movies)
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
df1 = pd.DataFrame(movie_list['genre'].apply(lambda x : x.split(",")))  
genre = set()
for i in range(9614):
    for j in df1['genre'][i]:
        genre.add(j)
df2 = pd.DataFrame(movie_list['orig_lang'].apply(lambda x : x.split()))  
Language = set()
for i in range(9614):
    for j in df2['orig_lang'][i]:
        Language.add(j)
# df3 = pd.DataFrame(movie_list['country'].apply(lambda x : x.split()))  
# country = set()
# for i in range(9614):
#     for j in df3['country'][i]:
#         country.add(j)
country = {'Philippines':'PH','United Kingdom':'GB',' Dominican Republic':'DO','Poland':'PL','India':'IN','Peru':'PE','France':'FR','Belgium':'BE',
           'Singapore':'SG','Thailand':'TH','China':'CN','Netherlands':'NL','Norway':'NO','Chile':'CL','Uruguay':'UY','South Korea':'KR', 'Boliva':'BO', 
           'Czech Republic':'XC','Ireland':'IE','Australia':'AU','Mexico':'MX','Japan':'JP','Denmark':'DK','Austria':'AT','Colombia':'CO','Paraguay':'PY', 
           'USSR':'SU','Finland':'FI','Indonesia':'ID','Greece':'GR','Italy':'IT','United States':'US','Turkey':'TR','Taiwan':'TW','Switzerland':'CH',
           'Mauritius':'MU','Slovakia':'SK','Israel':'IL','Portugal':'PT','Hong Kong':'HK','Myanmar':'MY','Brazil':'BR','Sweden':'SE','Spain':'ES','Argentina':'AR',
            'South Africa':'ZA','Germany':'DE','Czechia':'CZ','Ukraine':'UA','Vietnam':'VN','Canada':'CA','Hungary':'HU','Russia':'RU','Guatemala':'GT','Puerto Rico':'PR','Iceland':'IS'}
year = set(movie_list['Release_year'])
with st.container():
    selected_items = []
    selected_gener = st.selectbox(
    "Type or select a gener from the dropdown",
    genre
)
    selected_lang = st.selectbox(
    "Type or select a language from the dropdown",
    Language
)
    selected_country = st.selectbox(
    "Type or select a country the dropdown",
    country
)
    selected_year = st.selectbox(
    "Type or select a year the dropdown",
    year
)
if st.button('Filtter'):
    poster = []
    arr = movie_list[(movie_list['Release_year'] == selected_year) | (movie_list['country'] == country[selected_country]) | (movie_list['genre'] == selected_gener) | (movie_list['orig_lang'] == selected_lang)]
        # for i in arr['names'].values[0:9]:
        #     poster.append(fetch_poster(i))
    for i in range(10):
        with st.container():
            col3,col4 = st.columns(2)
            with col3:
                st.write(arr['names'].values[i])
                st.image("https://static.streamlit.io/examples/cat.jpg")
                # st.image(poster[i]) 
            with col4:
                st.write(arr['overview'].values[i])