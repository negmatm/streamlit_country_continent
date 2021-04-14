from numpy.lib.type_check import _nan_to_num_dispatcher
import streamlit as st
import pandas as pd
import math
import random
from streamlit import caching
from streamlit.script_runner import RerunException
from streamlit.script_request_queue import RerunData

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

st.title("Which continent is " + random_country + " in?")

chosen_continent = st.radio("",("I don't know", "Africa", "Asia", "Europe", "Eurasia", "North America", "South America", "Oceania"))

if st.button("Submit your answer"):
    if chosen_continent == continent_of_random_country:
        caching.clear_cache()
        st.write("This is correct!")
        st.balloons()
    else:
        st.warning("This is not correct.  Try again!")

if st.button("Another question please"):
    caching.clear_cache()
    raise RerunException(RerunData())
    
