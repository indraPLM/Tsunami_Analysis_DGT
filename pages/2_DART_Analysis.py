import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Tsunami Analysis - DART Buoys")

# Upload or fetch DART buoy data
uploaded_file = st.file_uploader("Upload DART Buoy Data (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    # Visualization
    st.subheader("Signal Visualization")
    time_col = st.selectbox("Select Time Column", options=df.columns)
    value_col = st.selectbox("Select Value Column", options=df.columns)

    fig, ax = plt.subplots()
    ax.plot(df[time_col], df[value_col], label=value_col)
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.set_title("DART Buoy Signal")
    ax.grid(True)
    st.pyplot(fig)
