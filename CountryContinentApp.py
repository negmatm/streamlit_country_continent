from numpy.lib.type_check import _nan_to_num_dispatcher
import streamlit as st
import pandas as pd
import math
import random
from streamlit import caching
from streamlit.script_runner import RerunException
from streamlit.script_request_queue import RerunData
import requests
import pydeck as pdk
import numpy as np

@st.cache
def load_countries():
    return pd.read_csv("Countries.csv")

@st.cache
def get_random_country_continent():
    random_number = math.floor((random.random()) * len(countries))
    return list(countries.iloc[random_number])

countries = load_countries()

random_country_continent = get_random_country_continent()
random_country = random_country_continent[0]
continent_of_random_country = random_country_continent[1]

response = requests.get(f"https://restcountries.eu/rest/v2/name/{random_country}")

capital_of_random_country = response.json()[0]["capital"]
location = response.json()[0]["latlng"]
location_latitude = location[0]
location_longitude = location[1]

game_option = st.sidebar.radio("Choose game option",("Continent", "Capital"))
st.sidebar.title("About")
st.sidebar.info("This app, which tests your knowledge of continents and capitals of countries, is maintained by Negmat Mullodzhanov")

if game_option == "Continent":

    st.title("Which continent is " + random_country + " in?")

    chosen_continent = st.radio("",("Africa", "Asia", "Europe", "Eurasia", "North America", "South America", "Oceania"))

    if st.button("Submit your answer"):
        if chosen_continent == continent_of_random_country:
            caching.clear_cache()
            st.write("This is correct!")
            st.balloons()
        else:
            st.warning("This is not correct.  Try again!")

    if st.button("I don't know"):
        st.write("The answer is: " + continent_of_random_country)

    if st.button("Show me the map please!"):

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(latitude=location_latitude,longitude=location_longitude,zoom=2.6)
        ))

    if st.button("Another question please"):
        caching.clear_cache()
        raise RerunException(RerunData())

elif game_option == "Capital":
    st.title("What is the capital of " + random_country + "?")

    entered_capital = st.text_input("Enter Capital")

    if st.button("Submit your answer"):
        if entered_capital == capital_of_random_country:
            caching.clear_cache()
            st.write("This is correct!")
            st.balloons()
        else:
            st.warning("This is not correct.  Try again!")

    if st.button("I don't know"):
        st.write("The answer is: " + capital_of_random_country)

    if st.button("Show me the map please!"):
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(latitude=location_latitude,longitude=location_longitude,zoom=6)
        ))

    if st.button("Another question please"):
        caching.clear_cache()
        raise RerunException(RerunData())
