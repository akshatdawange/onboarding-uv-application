from supabase import create_client, Client
import streamlit as st
import pandas as pd
import time

# Initializing Supabase
def get_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase()

# Params for OpenWeatherMap API
API_KEY = st.secrets["API_KEY"]
CITY_NAME = "Melbourne"
COUNTRY_CODE = "AU"
LIMIT = "5"

# Accessing Location Data
location_resp = supabase.table("Australian-States-and-Localities").select("*").execute()
location_data = location_resp.data

# Accessing the Cancer Statistics Data
cancer_stat_data = supabase.table("sun-safety").select("*").execute()
df = pd.DataFrame(cancer_stat_data.data)

# Setting the options for City selection
options = [f"{row['locality']}, {row['state']}" for row in location_data]

# Mapping each locality to the corresponding State
location_map = {
    f"{row['locality']}, {row['state']}": row
    for row in location_data
}

# Setting UNIX time for maintaining consistency for time sensitive data
TIMESTAMP = int(time.time())
Y_TIMESTAMP = TIMESTAMP - 86400