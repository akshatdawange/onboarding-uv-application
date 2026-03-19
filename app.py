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
import streamlit_authenticator as stauth

def creds_entered():
    if st.session_state["user"].strip() == st.secrets["ROOT_USER"] and st.session_state['pwd'].strip() == st.secrets["ROOT_PASS"]:
        st.session_state['authenticated'] = True
    else:
        st.session_state['authenticated'] = False

def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label="Username: ", value="", key="user", on_change=creds_entered)
        st.text_input(label="Password: ", value="", key="pwd", type="password", on_change=creds_entered)
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label="Username: ", value="", key="user", on_change=creds_entered)
            st.text_input(label="Password: ", value="", key="pwd", type="password", on_change=creds_entered)
            return False
    
if authenticate_user():

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
        <div class="main-title">☀️ Suns Protection Board</div>
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
