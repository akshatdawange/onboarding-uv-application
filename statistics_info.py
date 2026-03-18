import streamlit as st
from db import * 
from functions import *
import plotly.express as px

def stats():
    st.markdown("## 📊 Statistics Dashboard")

    # Cancer statistics first
    st.markdown("### Skin Cancer Statistics")
    st.markdown("Distribution of reported skin cancer cases across age groups.")

    df["Count"] = df["Count"].astype(int)
    df["Age Group"] = df["Age Group"].apply(lambda x: x.replace("‚Äì", " to "))

    grouped = df.groupby(["Type", "Age Group"])["Count"].sum().reset_index()

    fig_cancer = px.bar(
        grouped,
        x="Age Group",
        y="Count",
        color="Type",
        title="Cancer Cases by Age Group",
        labels={
            "Age Group": "Age Group",
            "Count": "Number of Cases",
            "Type": "Cancer Type"
        },
        barmode="group"
    )

    fig_cancer.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=20),
        legend=dict(orientation="h", y=-0.2)
    )

    st.plotly_chart(fig_cancer, use_container_width=True)

    st.write(
        "This chart shows how different skin cancer types are distributed across age groups. "
        "Use the legend to focus on individual cancer types."
    )

    st.markdown("---")

    # Placeholder for next feature
    st.markdown("### Yet to be developed")