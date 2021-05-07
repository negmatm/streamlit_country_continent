import streamlit as st
import pandas as pd
import math
import random
from streamlit import caching
from streamlit.script_runner import RerunException
from streamlit.script_request_queue import RerunData
import pydeck as pdk

@st.cache
def load_country_details():
    return pd.read_csv("CountriesExpanded.csv")

@st.cache
def get_random_row_from_file():
    random_number = math.floor((random.random()) * len(country_details))
    return list(country_details.iloc[random_number])

@st.cache(allow_output_mutation=True)
def get_random_capitals(how_many):
    random_capitals = set()

    for _ in range(how_many):
        random_number = math.floor((random.random()) * len(capital_list))
        random_capitals.add(capital_list[random_number])

    return random_capitals

country_details = load_country_details()
capital_list = list(country_details["capital"])

game_option = st.sidebar.radio("Choose game option",("Learn", "Quiz"))
st.sidebar.title("About")
st.sidebar.info("This app helps you learn facts about world's countries and also tests your knowledge.  It is maintained by Negmat Mullodzhanov")

if game_option == "Learn":
    st.title("Learn Georgraphy!")
    country = st.selectbox("Choose a country", list(country_details["country"]))
    country_row = country_details[country_details["country"] == country]

    continent = country_row["continent"].to_string(index = False)
    capital = country_row["capital"].to_string(index = False)
    latitude = float(country_row["latitude"])
    longitude = float(country_row["longitude"])
    flag_url = country_row["flag_url"].to_string(index = False)

    st.text("Continent: " + continent)
    st.text("Capital: " + capital)

    st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(latitude=latitude,longitude=longitude,zoom=5)
    ))

if game_option == "Quiz":
    st.title("Georgraphy Quiz!")
    random_row = get_random_row_from_file()
    country = random_row[0]
    continent = random_row[1]
    capital = random_row[2]
    latitude = random_row[3]
    longitude = random_row[4]
    flag_url = random_row[5]

    quiz_option = st.radio("Choose quiz option",("Continent", "Capital"))

    if quiz_option == "Continent":
        st.subheader("What continent is " + country + " on?")

        chosen_continent = st.radio("",("Africa", "Asia", "Europe", "Eurasia", "North America", "South America", "Oceania"))

        if st.button("Submit your answer"):
            if chosen_continent == continent:
                st.write("This is correct!")
                st.balloons()
                caching.clear_cache()
            else:
                st.warning("This is not correct.  Try again!")

        if st.button("I don't know"):
            st.write("The answer is: " + continent)

        if st.button("Show me the map please!"):

            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(latitude=latitude,longitude=longitude,zoom=2.5)
            ))

        if st.button("Another question please"):
            caching.clear_cache()
            raise RerunException(RerunData())

    elif quiz_option == "Capital":
        st.subheader("What is the capital of " + country + "?")

        capital_choices = get_random_capitals(3)
        capital_choices.add(capital)
        capital_choices = sorted(list(capital_choices))

        chosen_capital = st.radio("Choose a capital", capital_choices)

        if st.button("Submit your answer"):
            if chosen_capital == capital:
                st.write("This is correct!")
                st.balloons()
                caching.clear_cache()
            else:
                st.warning("This is not correct.  Try again!")

        if st.button("I don't know"):
            st.write("The answer is: " + capital)

        if st.button("Show me the map please!"):
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(latitude=latitude,longitude=longitude,zoom=6)
            ))

        if st.button("Another question please"):
            caching.clear_cache()
            raise RerunException(RerunData())
