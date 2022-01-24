import streamlit as st
import pickle
import requests


def fetch_movie_details(mov_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        mov_id)
    data = requests.get(url)
    data = data.json()
    return data


def fetch_poster(mov_id):
    data = fetch_movie_details(mov_id)
    poster = data['poster_path']
    movie_image = "https://image.tmdb.org/t/p/w500/" + poster
    return movie_image


def fetch_overview(mov_id):
    data = fetch_movie_details(mov_id)
    return data['overview']


def fetch_tagline(mov_id):
    data = fetch_movie_details(mov_id)
    return data['tagline']


def fetch_date(mov_id):
    data = fetch_movie_details(mov_id)
    release_date = data['release_date']
    return f"Release Date: {release_date}"


def get_recommendation(movie, no):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    movie_names = []
    movie_posters = []
    overviews = []
    taglines = []
    date = []

    for i in distances[1:no + 1]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_posters.append(fetch_poster(movie_id))
        movie_names.append(movies.iloc[i[0]].title)
        overviews.append(fetch_overview(movie_id))
        taglines.append(fetch_tagline(movie_id))
        date.append(fetch_date(movie_id))

    return movie_names, movie_posters, overviews, taglines, date


st.header('Teispace Movie Recommendation')
movies = pickle.load(open('model/movies.pkl', 'rb'))
similarity = pickle.load(open('model/similarities.pkl', 'rb'))

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Select/Enter Movie",
    movie_list
)

no_of_result = st.slider("No of Recommendations", min_value=3, max_value=10, value=5)


if st.button('Show Recommendation'):
    movie_names, movie_posters, overviews, taglines, date = get_recommendation(selected_movie, no_of_result)
    st.header(f"Recommendations for {selected_movie} are: ")
    st.title("")
    for i in range(len(movie_names)):
        st.title("")
        image, details = st.columns(2)
        with image:
            st.image(movie_posters[i])
        with details:
            st.title(movie_names[i])
            st.warning(taglines[i])
            st.subheader("Overview")
            st.info(overviews[i])
            st.warning(date[i])

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
