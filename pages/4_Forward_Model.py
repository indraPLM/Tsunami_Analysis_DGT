import streamlit as st

st.title("🌀 Forward Tsunami Propagation Model")

st.markdown("Define fault parameters to simulate tsunami wave propagation.")

# Example parameters
length = st.slider("Fault Length (km)", 10, 200, 100)
width = st.slider("Fault Width (km)", 10, 100, 50)
slip = st.slider("Slip Amount (m)", 0.1, 20.0, 2.0)
depth = st.slider("Depth (km)", 5, 50, 20)

st.button("Run Simulation")

# Placeholder output
st.markdown("🖼️ Simulated tsunami wave field would appear here.")
# You could visualize synthetic results using matplotlib or image overlays
