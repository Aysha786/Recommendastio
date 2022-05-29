import pickle
import requests
import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie

def load_lottieur(url):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances=similarity[index]
    movies_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

st.set_page_config(page_title="My Webpage",page_icon=":tada",layout="wide")
st.header("Hello!...I am Recommendatsio")
st.title("A Movie Recommendation system")
st.write("I'll give you my best five movie recommendations based on your tastes.")
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

lotty=load_lottieur("https://assets7.lottiefiles.com/private_files/lf30_bb9bkg1h.json")
st_lottie(lotty,height=300,key="coding")

# def get_movie_info(movie_id):
#     url = 'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id)
#     data=requests.get(url)
#     data=data.json()
#     s_data = BeautifulSoup(url_data, 'html.parser')
#     imdb_content = s_data.find("meta", property="og:description")
#     movie_descr = imdb_content.attrs['content']
#     movie_descr = str(movie_descr).split('.')
#     movie_director = movie_descr[0]
#     movie_cast = str(movie_descr[1]).replace('With', 'Cast: ').strip()
#     movie_story = 'Story: ' + str(movie_descr[2]).strip()+'.'
#     rating = s_data.find("div", class_="AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3 jkCVKJ")
#     rating = str(rating).split('<div class="AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3 jkCVKJ')
#     rating = str(rating[1]).split("</div>")
#     rating = str(rating[0]).replace(''' "> ''', '').replace('">', '')
#
#
# movie_rating = 'Total Rating count: '+ rating
# return movie_director,movie_cast,movie_story,movie_rating
#
# st.success('Some of the movies from our Recommendation, have a look below')
#  for movie, link, ratings in table:
#

# image = Image.open('sunrise.jpg')
#
# st.image(image, caption='Sunrise by the mountains')
# with right_column:
#     st_lottie(lotty,height=300,key="coding")

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
