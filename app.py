import requests
import streamlit as st
import time
from db import *
import geocoder
import pandas as pd
import plotly.express as px
from functions import *
from currentlocationinformation import *
from statistics_info import *
from prevention_info import *

st.set_page_config(
    page_title="Sun Protection Board",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load the custom CSS
load_css("styles.css")

# Header Banner
st.markdown("""
<div class="hero-card">
    <div class="main-title">☀️ Sun Protection Board</div>
    <div class="sub-title">
        Real-time UV, temperature, and sun safety insights to help users stay protected.
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs which go to different sections
CurrentLocationInformation, Statistics, PreventionMethods = st.tabs(
    ["Current Location Information", "Statistics", "Prevention Methods"]
)

# Section 1 : Displaying location based information
with CurrentLocationInformation:
    currentlocationinfo()

# Section 2 : Displaying Statistical Information
with Statistics:
    stats()

with PreventionMethods:
    prevention_techniques()