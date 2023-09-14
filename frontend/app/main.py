from widget.movie import MovieWidgets
from service.movies_api import MoviesApi
import streamlit as st
from cache.session_state import init_session_state

st.title("Movie Recomendator🎬")

st.image("https://static.amazon.jobs/teams/53/images/IMDb_Header_Page.jpg?1501027252")

init_session_state()


if st.session_state.current_movie is not None:
    _, c1, _ = st.columns((0.5, 1, 0.5))
    c2, c3 = st.columns(2)

    st.session_state.recomendations = MoviesApi.get_recomendation(
        st.session_state.current_movie, st.session_state.blacklist
    )
    with c1:
        MovieWidgets.display_movie(st.session_state.current_movie)

    with c3:
        if st.button("👍", use_container_width=True):
            st.session_state.blacklist.append(st.session_state.current_movie)
            st.session_state.current_movie = st.session_state.recomendations[
                st.session_state.recomendation_threshold["like"]
            ]
            st.experimental_rerun()
    with c2:
        if st.button("👎", use_container_width=True):
            st.session_state.blacklist.append(st.session_state.current_movie)
            st.session_state.current_movie = st.session_state.recomendations[
                st.session_state.recomendation_threshold["dislike"]
            ]
            st.experimental_rerun()
    threshold = st.select_slider("Threshold", options=range(0, 31))
    st.session_state.recomendation_threshold["like"] = threshold
    st.session_state.recomendation_threshold["dislike"] = (threshold + 1) * -1

my_expander = st.expander("Selecione um filme 🎬")
selected_movie_name = my_expander.selectbox("", MoviesApi.get_all_movies())

if my_expander.button("Recomendar"):
    st.text("Recomendações..")
    st.write("#")
    recomendations = MoviesApi.get_recomendation(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for i in range(0, 5):
        with cols[i]:
            MovieWidgets.display_movie(recomendations[i])

if st.button("Start App 🎲", use_container_width=True):
    st.session_state.current_movie = MoviesApi.get_random_movie()
    st.session_state.blacklist = []
    st.experimental_rerun()


st.markdown(f"##### Blacklist Size: {len(st.session_state.blacklist)}")
