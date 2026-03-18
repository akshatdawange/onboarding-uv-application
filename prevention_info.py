import streamlit as st
from db import *
from functions import *


def prevention_techniques():

    st.markdown("## 🛡 UV Clothing and Protection Guide")
    st.markdown("Select a UV category to view recommended clothing and protective measures.")

    uv_guide = get_manual_uv_guide()

    class_map = {
        "Low": "uv-strip-low",
        "Moderate": "uv-strip-moderate",
        "High": "uv-strip-high",
        "Very High": "uv-strip-very-high",
        "Extreme": "uv-strip-extreme"
    }

    for level in ["Low", "Moderate", "High", "Very High", "Extreme"]:
        info = uv_guide[level]
        strip_class = class_map[level]

        st.markdown(
            f"""
            <div class="uv-strip {strip_class}">
                {level} ({info['range']})
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander(f"Open {level} guide"):
            st.markdown("### Recommended Clothing")
            for item in info["clothing"]:
                st.markdown(f"- {item}")

            st.markdown("### Protective Measures")
            for item in info["protection"]:
                st.markdown(f"- {item}")