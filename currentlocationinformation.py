import streamlit as st
from functions import *
from db import *

def currentlocationinfo():
    mode = st.radio(
            "Choose location source",
            ["Use Current Location", "Select From List"],
            horizontal=True,
            key="location_mode"
        )

    if mode == "Use Current Location":
            left_panel, right_panel = st.columns([1.15, 1], gap="large")

            with left_panel:
                st.markdown("""
                <div class="top-panel">
                    <div class="panel-title">📍 Current Location Overview</div>
                    <div class="panel-text">
                        Use your device location to get live UV index and temperature
                        for where you are right now.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                current_loc_clicked = st.button(
                    "Use Current Location",
                    key="current_location_btn",
                    use_container_width=True
                )

            with right_panel:
                st.markdown("""
                <div class="top-panel">
                    <div class="panel-title">ℹ️ How it works</div>
                    <div class="panel-text">
                        This option uses your detected location and shows current
                        temperature and UV conditions for your area only.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if current_loc_clicked:
                coordinates = get_current_gps_coordinates()

                if coordinates is not None:
                    lat, lon = coordinates

                    if lat and lon:
                        weather_data = fetch_weather_data(lat, lon, API_KEY, Y_TIMESTAMP)
                        st.markdown("### Results for Your Current Location")
                        show_weather_cards(weather_data)
                    else:
                        st.warning("Unable to retrieve valid coordinates.")
                else:
                    st.warning("Unable to retrieve your current location.")

    elif mode == "Select From List":
            left_panel, right_panel = st.columns([1.15, 1], gap="large")

            with left_panel:
                st.markdown("""
                <div class="top-panel">
                    <div class="panel-title">🏙️ Locality Comparison</div>
                    <div class="panel-text">
                        Select a locality from the list to view its current UV index and
                        temperature conditions.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with right_panel:
                st.markdown("""
                <div class="top-panel">
                    <div class="panel-title">🌍 Select a Location</div>
                    <div class="panel-text">
                        Choose one city from the database and fetch weather insights
                        only for that selected place.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                selected = st.selectbox(
                    "Select City",
                    options=options,
                    index=None,
                    placeholder="Choose a city",
                    key="city_selectbox"
                )

            st.markdown("<br>", unsafe_allow_html=True)

            if selected:
                lat_selc = location_map[selected]["lat"]
                lon_selc = location_map[selected]["long"]

                if lat_selc and lon_selc:
                    weather_data = fetch_weather_data(lat_selc, lon_selc, API_KEY, Y_TIMESTAMP)
                    st.markdown(f"### Results for {selected}")
                    show_weather_cards(weather_data)