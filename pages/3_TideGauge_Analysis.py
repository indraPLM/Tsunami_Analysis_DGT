import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utide import solve, reconstruct

st.title("📈 Tsunami Analysis - Tide Gauge")

uploaded_file = st.file_uploader("Upload Tide Gauge Data (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    time_col = st.selectbox("Time Column", options=df.columns)
    height_col = st.selectbox("Water Level Column", options=df.columns)

    # UTide detiding
    st.subheader("Harmonic Analysis (UTide)")
    coef = solve(df[time_col], df[height_col], lat=0, method='ols')
    tide, _ = reconstruct(df[time_col], coef)

    fig, ax = plt.subplots(2, 1)
    ax[0].plot(df[time_col], df[height_col], label="Observed")
    ax[0].plot(df[time_col], tide, label="Predicted", alpha=0.6)
    ax[0].legend()
    ax[0].set_title("Observed vs Predicted Tide")
    
    anomaly = df[height_col] - tide
    ax[1].plot(df[time_col], anomaly, color="red")
    ax[1].set_title("Tsunami Signal (Anomaly)")
    st.pyplot(fig)
