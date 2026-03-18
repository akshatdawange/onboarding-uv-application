import streamlit as st
import geocoder
import requests
import plotly.graph_objects as go
import time

# Accessing the custom CSS file for all the customizations
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Accessing the user Lat and Long information based on IP Address
def get_current_gps_coordinates():
    g = geocoder.ip('me')
    if g.latlng is not None:
        return g.latlng
    else:
        return None

# Setting the classes of the UV Index levels
def get_uv_class(uvi):
    if uvi <= 2:
        return "uv-low", "Low"
    elif uvi <= 5:
        return "uv-moderate", "Moderate"
    elif uvi <= 7:
        return "uv-high", "High"
    elif uvi <= 10:
        return "uv-very-high", "Very High"
    else:
        return "uv-extreme", "Extreme"

# Setting the classes of the Temperature Levels
def get_temp_class(temp_c):
    if temp_c < 10:
        return "temp-cold", "Cold"
    elif temp_c < 20:
        return "temp-mild", "Mild"
    elif temp_c < 30:
        return "temp-warm", "Warm"
    else:
        return "temp-hot", "Hot"
    
# Custom HTML code to render the metrics cards
def render_metric_card(label, value, delta_text, subtext="", icon="📊", card_class="", delta_value=0):
    delta_color = "#ff6b6b" if delta_value > 0 else "#7dd3fc"

    st.markdown(f"""
    <div class="metric-card {card_class}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta" style="color: {delta_color};">{delta_text}</div>
        <div class="metric-subtext">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)

# Fetching the Weather Data from the API
def fetch_weather_data(lat, lon, api_key, y_timestamp):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"
    history_url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={y_timestamp}&appid={api_key}"

    response = requests.get(url)
    response2 = requests.get(history_url)

    data = response.json()
    y_data = response2.json()

    current = data["current"]

    temp_c = current["temp"] - 273.15
    yesterday_temp_c = y_data["data"][0]["temp"] - 273.15

    uvi = current["uvi"]
    uvi_yest = y_data["data"][0]["uvi"]

    description = current["weather"][0]["description"]

    delta_temp = temp_c - yesterday_temp_c
    delta_uvi = uvi - uvi_yest

    return {
        "temp_c": temp_c,
        "yesterday_temp_c": yesterday_temp_c,
        "uvi": uvi,
        "uvi_yest": uvi_yest,
        "description": description,
        "delta_temp": delta_temp,
        "delta_uvi": delta_uvi,
    }

# Custom cards for the UV protection techniques
def get_uv_details(uvi):
    if uvi <= 2:
        return {
            "label": "Low",
            "color": "#22c55e",
            "advice": [
                "Minimal protection required",
                "Wear sunglasses if outdoors for long periods",
                "Use sunscreen for extended outdoor exposure"
            ]
        }
    elif uvi <= 5:
        return {
            "label": "Moderate",
            "color": "#eab308",
            "advice": [
                "Use SPF 30+ sunscreen",
                "Wear sunglasses",
                "Consider a hat during midday hours"
            ]
        }
    elif uvi <= 7:
        return {
            "label": "High",
            "color": "#f97316",
            "advice": [
                "Use SPF 50+ sunscreen",
                "Wear a wide-brim hat",
                "Use sunglasses and seek shade when possible"
            ]
        }
    elif uvi <= 10:
        return {
            "label": "Very High",
            "color": "#ef4444",
            "advice": [
                "SPF 50+ sunscreen is strongly recommended",
                "Wear protective clothing, hat, and sunglasses",
                "Reduce time in direct sunlight, especially midday"
            ]
        }
    else:
        return {
            "label": "Extreme",
            "color": "#d946ef",
            "advice": [
                "Avoid direct sun exposure if possible",
                "Use SPF 50+ and reapply frequently",
                "Stay in shade, wear full protection, and avoid peak UV hours"
            ]
        }

# Semi circular gauge to show the UV index on a scale
def render_uv_circular_scale(uvi):
    uv_info = get_uv_details(uvi)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=uvi,
        number={"font": {"size": 42, "color": "white"}},
        title={"text": f"UV Risk • {uv_info['label']}", "font": {"size": 22, "color": "white"}},
        gauge={
            "axis": {"range": [0, 12], "tickwidth": 1, "tickcolor": "white"},
            "bar": {"color": uv_info["color"], "thickness": 0.28},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 2], "color": "rgba(34, 197, 94, 0.28)"},
                {"range": [2, 5], "color": "rgba(234, 179, 8, 0.28)"},
                {"range": [5, 7], "color": "rgba(249, 115, 22, 0.28)"},
                {"range": [7, 10], "color": "rgba(239, 68, 68, 0.28)"},
                {"range": [10, 12], "color": "rgba(217, 70, 239, 0.28)"}
            ],
            "threshold": {
                "line": {"color": "white", "width": 5},
                "thickness": 0.8,
                "value": uvi
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
        margin=dict(t=60, b=20, l=20, r=20),
        height=380
    )

    st.plotly_chart(fig, use_container_width=True)

# Recommendation card for protection
def render_uv_prevention_card(uvi):
    uv_info = get_uv_details(uvi)

    advice_html = "".join([f"<li>{item}</li>" for item in uv_info["advice"]])

    st.markdown(
        f"""
        <div class="advice-card">
            <div class="advice-title">Protection Advice</div>
            <div class="advice-subtitle">
                Recommended prevention methods based on the current UV level.
            </div>
            <div class="advice-pill" style="background:{uv_info['color']};">
                {uv_info['label']} Risk
            </div>
            <ul class="advice-list">
                {advice_html}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# Temperature and UV levels cards
def show_weather_cards(weather_data):
    temp_c = weather_data["temp_c"]
    uvi = weather_data["uvi"]
    delta_temp = weather_data["delta_temp"]
    delta_uvi = weather_data["delta_uvi"]
    description = weather_data["description"]

    uv_class, uv_label = get_uv_class(uvi)

    metric_col1, metric_col2 = st.columns(2, gap="large")

    with metric_col1:
        delta_prefix_temp = "+" if delta_temp > 0 else ""
        temp_class, temp_label = get_temp_class(temp_c)

        render_metric_card(
        label=f"Temperature • {temp_label}",
        value=f"{temp_c:.1f} °C",
        delta_text=f"{delta_prefix_temp}{delta_temp:.1f} °C vs yesterday",
        subtext=f"Conditions: {description.capitalize()}",
        icon="🌡️",
        card_class=temp_class,
        delta_value=delta_temp
    )

    with metric_col2:
        delta_prefix_uvi = "+" if delta_uvi > 0 else ""
        render_metric_card(
            label=f"UV Index • {uv_label}",
            value=f"{uvi:.1f}",
            delta_text=f"{delta_prefix_uvi}{delta_uvi:.1f} vs yesterday",
            subtext="Current sun exposure intensity",
            icon="☀️",
            card_class=uv_class,
            delta_value=delta_uvi
        )

    st.markdown("### UV Protection Overview")

    gauge_col, advice_col = st.columns([1.1, 1], gap="large")

    with gauge_col:
        render_uv_circular_scale(uvi)

    with advice_col:
        render_uv_prevention_card(uvi)

    if uvi < 2:
        st.toast("Low risk of UV harm today!")
        time.sleep(2)
    elif 2 < uvi <= 5:
        st.toast("Moderate risk of UV harm today. Stay protected.")
        time.sleep(2)
    elif 5 < uvi <= 7:
        st.toast("Higher risk of UV harm today. Use appropriate protection methods.")
        time.sleep(2)
    elif uvi > 8:
        st.toast("Extreme risk of UV harm. Avoid stepping out in the sun. Use appropriate protection methods.")
        time.sleep(2)

# Clothing recommendations for the prevention methods
def get_clothing_recommendation(uvi):
    if uvi <= 2:
        return {
            "label": "Low",
            "color": "#22c55e",
            "clothes": [
                "A regular T-shirt or light top is generally suitable",
                "Lightweight everyday clothing is enough for most short outdoor activities",
                "Optional light cover such as a cap if staying outside for longer"
            ],
            "accessories": [
                "Sunglasses optional",
                "Hat optional for extended exposure"
            ],
            "tip": "UV is low, so basic protection is usually enough unless you plan to stay outdoors for a long time."
        }

    elif uvi <= 5:
        return {
            "label": "Moderate",
            "color": "#eab308",
            "clothes": [
                "Wear a sleeved T-shirt, polo, or top that covers the shoulders",
                "Choose breathable fabrics that still provide some coverage",
                "Avoid outfits that leave large areas of skin exposed for long periods"
            ],
            "accessories": [
                "Wear sunglasses",
                "Use a cap or hat when outdoors around midday"
            ],
            "tip": "Moderate UV calls for practical sun-smart clothing that still feels comfortable in warm weather."
        }

    elif uvi <= 7:
        return {
            "label": "High",
            "color": "#f97316",
            "clothes": [
                "Prefer long-sleeved or more covering clothing",
                "Choose lightweight but protective fabrics",
                "Aim to cover shoulders, upper arms, and as much skin as practical"
            ],
            "accessories": [
                "Wear a wide-brim hat",
                "Wear sunglasses with good UV protection"
            ],
            "tip": "At high UV levels, clothing should provide stronger skin coverage while staying cool and breathable."
        }

    elif uvi <= 10:
        return {
            "label": "Very High",
            "color": "#ef4444",
            "clothes": [
                "Wear lightweight long-sleeved clothing with maximum practical coverage",
                "Choose tightly woven fabrics to improve sun protection",
                "Loose-fitting clothing is recommended to stay cooler"
            ],
            "accessories": [
                "Wear a wide-brim hat",
                "Wear sunglasses",
                "Use extra protection for exposed areas"
            ],
            "tip": "Very high UV means your clothing should balance breathability with strong sun coverage."
        }

    else:
        return {
            "label": "Extreme",
            "color": "#d946ef",
            "clothes": [
                "Wear full-coverage sun-protective clothing where possible",
                "Use tightly woven, long-sleeved, loose-fitting garments",
                "Minimize exposed skin as much as possible"
            ],
            "accessories": [
                "Wear a wide-brim hat",
                "Wear UV-protective sunglasses",
                "Combine clothing protection with shade and sunscreen"
            ],
            "tip": "Extreme UV conditions require maximum protection. Full coverage is strongly recommended."
        }

# Prevention Methods clothing and accessories recommendations expanders
def render_clothing_recommendation(uvi):
    clothing_info = get_clothing_recommendation(uvi)

    clothes_html = "".join([f"<li>{item}</li>" for item in clothing_info["clothes"]])
    accessories_html = "".join([f"<li>{item}</li>" for item in clothing_info["accessories"]])

    st.markdown(
        f"""
        <div class="clothing-card">
            <div class="clothing-title">👕 What to Wear Today</div>
            <div class="clothing-subtitle">
                Clothing recommendations based on the current UV level.
            </div>

            <div class="clothing-pill" style="background:{clothing_info['color']};">
                {clothing_info['label']} UV Risk
            </div>

            <div class="clothing-section-heading">Recommended Clothing</div>
            <ul class="clothing-list">
                {clothes_html}
            </ul>

            <div class="clothing-section-heading">Suggested Accessories</div>
            <ul class="clothing-list">
                {accessories_html}
            </ul>

            <div class="clothing-tip">
                {clothing_info['tip']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Content for the expanders
def get_manual_uv_guide():
    return {
        "Low": {
            "range": "0–2",
            "color": "#22c55e",
            "card_class": "uv-low-card",
            "clothing": [
                "Regular light clothing is suitable",
                "A T-shirt or light top is usually enough",
                "Optional light cover if outdoors for long periods"
            ],
            "protection": [
                "Sunglasses optional",
                "Hat optional for long exposure",
                "Basic sunscreen is enough for extended outdoor time"
            ]
        },
        "Moderate": {
            "range": "3–5",
            "color": "#eab308",
            "card_class": "uv-moderate-card",
            "clothing": [
                "Wear a sleeved top that covers the shoulders",
                "Choose breathable clothing with some skin coverage",
                "Avoid staying in highly exposed outfits for too long"
            ],
            "protection": [
                "Wear sunglasses",
                "Use a cap or hat",
                "Apply sunscreen on exposed skin"
            ]
        },
        "High": {
            "range": "6–7",
            "color": "#f97316",
            "card_class": "uv-high-card",
            "clothing": [
                "Prefer long sleeves or more covering clothing",
                "Choose lightweight but protective fabric",
                "Cover shoulders and upper arms"
            ],
            "protection": [
                "Wear a wide-brim hat",
                "Wear UV-protective sunglasses",
                "Use sunscreen and seek shade when possible"
            ]
        },
        "Very High": {
            "range": "8–10",
            "color": "#ef4444",
            "card_class": "uv-very-high-card",
            "clothing": [
                "Wear lightweight long-sleeved clothing",
                "Use tightly woven and loose-fitting fabrics",
                "Try to maximize practical skin coverage"
            ],
            "protection": [
                "Wear a wide-brim hat",
                "Wear sunglasses",
                "Use sunscreen and avoid prolonged direct exposure"
            ]
        },
        "Extreme": {
            "range": "11+",
            "color": "#d946ef",
            "card_class": "uv-extreme-card",
            "clothing": [
                "Wear full-coverage sun-protective clothing",
                "Use tightly woven long-sleeved garments",
                "Minimize exposed skin as much as possible"
            ],
            "protection": [
                "Wear a wide-brim hat",
                "Wear UV-protective sunglasses",
                "Use sunscreen, seek shade, and avoid direct sun when possible"
            ]
        }
    }